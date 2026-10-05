"""Publish a small text-only feed. Authentication stays inside GitHub Actions."""
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import os
import re
import time

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'pageInfo { hasNextPage endCursor }'
FIELDS = 'id bodyText createdAt url isMinimized author { login }'
REPLIES = 'replies(first: 20) { nodes { ' + FIELDS + ' } ' + PAGE + ' }'
COMMENTS = 'comments(first: 50) { nodes { ' + FIELDS + ' ' + REPLIES + ' } ' + PAGE + ' }'
DISCUSSIONS_QUERY = '''query($owner:String!, $name:String!, $after:String) {
  repository(owner:$owner,name:$name) {
    discussions(first:25,after:$after,orderBy:{field:UPDATED_AT,direction:DESC}) {
      nodes { id title category { name } ''' + COMMENTS + ''' } ''' + PAGE + '''
    }
  }
}'''
COMMENTS_QUERY = '''query($id:ID!, $after:String) {
  node(id:$id) { ... on Discussion {
    comments(first:50,after:$after) { nodes { ''' + FIELDS + ' ' + REPLIES + ' } ' + PAGE + ''' }
  } }
}'''
REPLIES_QUERY = '''query($id:ID!, $after:String) {
  node(id:$id) { ... on DiscussionComment {
    replies(first:100,after:$after) { nodes { ''' + FIELDS + ' } ' + PAGE + ''' }
  } }
}'''


class GitHub:
    def __init__(self, token):
        self.token = token
        self.calls = 0

    def query(self, query, **variables):
        self.calls += 1
        if self.calls > 500:
            raise RuntimeError('Feed is too large for one run; previous feed is preserved.')
        payload = json.dumps({'query': query, 'variables': variables}).encode()
        for attempt in range(3):
            req = Request('https://api.github.com/graphql', data=payload, headers={
                'Authorization': 'Bearer ' + self.token,
                'Content-Type': 'application/json',
                'User-Agent': 'Pho-Blog-Comments-Feed',
            })
            try:
                with urlopen(req, timeout=45) as response:
                    result = json.load(response)
                if result.get('errors'):
                    raise RuntimeError('GitHub GraphQL: ' + '; '.join(e.get('message', 'Unknown error') for e in result['errors']))
                return result['data']
            except HTTPError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt == 2:
                    raise RuntimeError(f'GitHub API returned HTTP {exc.code}. Check Actions permissions.') from None
            except URLError:
                if attempt == 2:
                    raise RuntimeError('GitHub API is unavailable; previous feed is preserved.') from None
            time.sleep(2 ** (attempt + 1))


def pages(first, more):
    page = first
    seen = set()
    while True:
        yield from page['nodes']
        info = page['pageInfo']
        if not info['hasNextPage']:
            break
        cursor = info['endCursor']
        if not cursor or cursor in seen:
            raise RuntimeError('Invalid pagination cursor; previous feed is preserved.')
        seen.add(cursor)
        page = more(cursor)


def post_url(title, site_url):
    """Only accept article paths on this blog, never arbitrary discussion links."""
    base = urlsplit(site_url)
    path = unquote(str(title).strip())
    prefix = base.path.rstrip('/') + '/'
    if not path.startswith(prefix) or path == prefix:
        return None
    if any(c in path for c in ('?', '#', '\\')) or any(ord(c) < 32 for c in path):
        return None
    if any(part in {'.', '..'} for part in path.split('/')):
        return None
    if '%' in path:
        return None
    path = re.sub(r'/index\.html$', '/', path)
    return urlunsplit((base.scheme, base.netloc, quote(path, safe='/'), '', 'comments'))


def record(comment, post, reply=False):
    if not comment or comment.get('isMinimized'):
        return None
    body = re.sub(r'\s+', ' ', comment.get('bodyText', '')).strip()
    if not body:
        return None
    created = comment['createdAt']
    datetime.fromisoformat(created.replace('Z', '+00:00'))
    return {
        'id': comment['id'],
        'author': (comment.get('author') or {}).get('login', 'Deleted user'),
        'createdAt': created,
        'excerpt': body[:180] + ('…' if len(body) > 180 else ''),
        'postURL': post,
        'isReply': reply,
    }


def build(api, repo, config):
    owner, name = repo.split('/', 1)
    def discussions(after=None):
        data = api.query(DISCUSSIONS_QUERY, owner=owner, name=name, after=after)
        if not data.get('repository'):
            raise RuntimeError('Repository unavailable. Enable Discussions and check permissions.')
        return data['repository']['discussions']
    entries = {}
    for discussion in pages(discussions(), discussions):
        if not discussion or discussion['category']['name'] != config['category']:
            continue
        post = post_url(discussion['title'], config['siteURL'])
        if not post:
            continue
        def more_comments(cursor):
            return api.query(COMMENTS_QUERY, id=discussion['id'], after=cursor)['node']['comments']
        for comment in pages(discussion['comments'], more_comments):
            if not comment or comment.get('isMinimized'):
                continue
            item = record(comment, post)
            if item:
                entries[item['id']] = item
            def more_replies(cursor):
                return api.query(REPLIES_QUERY, id=comment['id'], after=cursor)['node']['replies']
            for reply in pages(comment['replies'], more_replies):
                item = record(reply, post, True)
                if item:
                    entries[item['id']] = item
    limit = max(1, min(int(config.get('limit', 20)), 50))
    items = sorted(entries.values(), key=lambda item: (item['createdAt'], item['id']), reverse=True)
    return {'schemaVersion': 1, 'comments': items[:limit]}


def main():
    token = os.environ.get('GH_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not token or not repo:
        raise SystemExit('Run this script in GitHub Actions with its built-in token.')
    config = json.loads((ROOT / 'feed-config.json').read_text(encoding='utf-8'))
    base = urlsplit(config['siteURL'])
    if base.scheme != 'https' or not base.netloc or not base.path.endswith('/'):
        raise SystemExit('siteURL must be an HTTPS URL with a trailing slash.')
    feed = build(GitHub(token), repo, config)
    destination = ROOT / 'recent-comments.json'
    temporary = destination.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(destination)
    print(f'Recent comments: {len(feed["comments"])}')


if __name__ == '__main__':
    main()
