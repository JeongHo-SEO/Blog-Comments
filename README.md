# Blog Comments

The public comment space for [Pho’s Technical Notes](https://jeongho-seo.github.io/Blog/), powered by [giscus](https://giscus.app).

## Join the conversation

Open a blog post and expand **Comments** to leave a question, share an idea, or suggest a correction. Sign in with GitHub to participate; your GitHub username and avatar will be visible with your comment.

- Read comments without signing in.
- React to a post with GitHub reactions, or use the blog’s Copy link button to share it without signing in.
- Choose **Oldest** or **Newest** to sort top-level comments when comments are present. Replies stay with their parent comment.
- Visit [Discussions](https://github.com/JeongHo-SEO/Blog-Comments/discussions) to browse conversations across posts.

## A few ground rules

Please keep comments relevant, respectful, and constructive. Questions and corrections are welcome. Spam, harassment, and unrelated promotion may be removed. Avoid posting passwords, contact details, or other information you do not want to make public.

## About this repository

This repository stores public blog discussions and the small integration files used to display recent comments. The blog’s source code is maintained separately; it is not included here.

Recent comment excerpts, GitHub usernames, timestamps, and links are published in `recent-comments.json` for the blog’s **Recent Comments** section. The feed is refreshed by GitHub Actions after discussion activity and on a daily fallback schedule. Updates may take a few minutes or longer when GitHub Actions is delayed. Deletions and moderation changes are reflected on a subsequent successful refresh; previously published versions may remain in Git history and caches.

## Maintenance

- `giscus.json`: permitted blog origin and default comment order.
- `feed-config.json`: blog URL, discussion category, and feed size.
- `scripts/build_recent_comments.py`: builds the public feed from visible comments and replies.
- `.github/workflows/recent-comments.yml`: runs the feed builder with the repository’s built-in token. No personal access token is required.

The feed workflow must be on the default `main` branch. Enable Discussions and use an **Announcements** category. To refresh manually, open **Actions → Update recent comments → Run workflow**.

## License

The original integration code and accompanying technical documentation in this repository are licensed under the [MIT License](LICENSE).

This license does not apply to visitor comments, discussion content, generated comment excerpts, or the blog’s articles. Those remain subject to their authors’ rights and applicable GitHub terms. Giscus is a separate project with its own license.
