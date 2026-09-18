# 6. Public support and privacy pages / 支持与隐私页面

## Reuse an existing domain when authorized

A small static support site is often enough. Example URLs:

- `https://example.com/example-app/`
- `https://example.com/example-app/support/`
- `https://example.com/example-app/privacy/`

Provide readable English and Chinese content, navigation between pages, an approved public support channel, and an effective date. The privacy page must describe actual app behavior, not generic “we value privacy” language. Link to it from both the app and App Store Connect.

Use a separate source directory/repository for the public pages when it makes ownership clearer. Avoid copying app signing material, private release receipts, deployment credentials or recordings into the web root. Never publish an unredacted build log as “support documentation.”

## Low-impact deployment pattern

The observed workflow reused an existing AWS-hosted domain and TLS setup, adding only an app-specific static prefix. The reusable pattern is independent of provider:

1. Inventory the authorized existing host/domain/router and baseline the sibling pages/APIs.
2. Build the static content locally; validate links, fragments, assets and bilingual mobile layout.
3. Compute a manifest of public files and SHA-256 hashes.
4. Copy a new immutable release directory. Expose only its public subdirectory.
5. Back up the exact relevant routing configuration and record the previously active release.
6. Add a prefix-specific route; syntax-check configuration before activation.
7. Activate atomically where supported, with a narrowly scoped reload when needed.
8. Poll the public HTTPS URLs until exact committed hashes match; then verify sibling behavior again.
9. Keep a rollback that refuses to overwrite unrelated later configuration changes.

Do not create new infrastructure, replace DNS/TLS, rebuild an unrelated frontend, restart application processes or change shared routes unless the task requires and authorizes it. An app support page should have a small, reviewable deployment footprint.

## Verify rendered content and transport

A 200 response alone is insufficient: it could be an old page or the site's catch-all route. Check exact public content hashes, proper slash/HTTPS redirects, valid TLS, and no accidental access to `.git`, private manifests, deployment scripts or nonexistent pages.

Inspect the actual site in a browser at mobile and desktop widths. Follow English/Chinese jump links, check the active navigation, load all images and ensure no horizontal overflow. Verify relevant headers, such as `nosniff` and an appropriate Content Security Policy; avoid unnecessary cookies or analytics.

Immediately after a server reload, an old worker can briefly return the previous version. Poll for the expected hash with a bounded timeout before declaring success or failure. Keep old and new content distinguishable; do not simply retry until any 200 appears.

## Privacy text that matters

State the owner/operator generically while drafting, then have the owner supply an approved public identity privately for the actual site. Explain local storage, explicit deletion, iOS backups, optional cloud transmission, provider terms/retention uncertainty, future opt-out and how support requests are handled. A private App Review phone number does not belong on a public support page.

Keep the claim “available on the App Store” and a download badge absent until release availability is verified. Support pages can exist before review without claiming launch.

Use [privacy-policy.md](../templates/privacy-policy.md) as an outline and keep deployment receipts private. This playbook deliberately contains no production host commands, IP addresses, account profile names or real server paths.

**中文要点：** 复用已经授权的域名与基础设施，只新增应用专属路径。发布后同时检查页面内容哈希、浏览器效果和其他站点健康；保留可回滚版本，不把私有部署文件放进公开目录。
