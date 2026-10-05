# Blog Comments

The public comment space for [Pho’s Technical Notes](https://jeongho-seo.github.io/Blog/), powered by [giscus](https://giscus.app).

## Join the conversation

Open a blog post and expand **Comments** to leave a question, share an idea, or suggest a correction.

- Read comments without signing in.
- Sign in with GitHub to comment or react. Your GitHub username and avatar are visible with your comments.
- Click **React** near the post header to choose a reaction.
- Choose **Oldest** or **Newest** to sort comments. Replies stay with their parent comment.
- Use **Copy URL** to copy the post link.
- Use **Share**, where supported, to open your device’s sharing menu.
- Visit [Discussions](https://github.com/JeongHo-SEO/Blog-Comments/discussions) to browse conversations across posts.

## Community guidelines

Please keep comments relevant, respectful, and constructive. Questions and corrections are welcome.

Spam, harassment, and unrelated promotion may be removed. Avoid posting passwords or other information you do not want to make public.

## About this repository

This repository hosts public blog discussions, reaction themes, and the integration files used to publish recent comments.

The blog’s source code is maintained separately and is not included here.

Recent comment excerpts, GitHub usernames, timestamps, and links are published in `recent-comments.json` for the blog’s **Recent Comments** section.

GitHub Actions refreshes this feed after supported discussion events and on a daily fallback schedule. Updates may take a few minutes or longer when GitHub Actions is delayed.

Deletions and moderation changes are reflected on a subsequent successful refresh. Previously published versions may remain in Git history and caches.

## Repository files

| File | Purpose |
| --- | --- |
| `giscus.json` | Allowed blog origin and default comment order |
| `feed-config.json` | Blog URL, discussion category, and feed size |
| `reactions-button-light.css` | Light theme for the post reaction button and picker |
| `reactions-button-dark.css` | Dark theme for the post reaction button and picker |
| `recent-comments.json` | Automatically generated recent comment feed |
| `scripts/build_recent_comments.py` | Builds the feed from visible comments and replies |
| `.github/workflows/recent-comments.yml` | Runs the feed builder and saves updates |

## Maintenance

Keep Discussions enabled and retain the discussion category configured in the blog and feed settings.

The feed workflow must be on the default `main` branch. It uses the repository’s built-in GitHub Actions token; no personal access token is required.

To refresh the feed manually, open **Actions → Update recent comments → Run workflow**.

Reaction theme changes do not need to run the recent comment workflow. Cached theme files may take time to update.

## License

The original integration code and accompanying technical documentation in this repository are licensed under the [MIT License](LICENSE).

This license does not apply to visitor comments, discussion content, generated comment excerpts, or the blog’s articles. Those remain subject to their authors’ rights and applicable GitHub terms.

Giscus is a separate project with its own license.
