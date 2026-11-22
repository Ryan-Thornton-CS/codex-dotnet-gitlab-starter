---
name: gitlab-pages-intake
description: Change the DocFX site on GitLab Pages or design a feature suggestion flow that lands GitLab issues on a project Kanban board.
---

Trace the DocFX build and Pages publish path before changing the site. Keep the developer API docs and the user guide/release pages distinct in navigation. Verify existing links, visibility, and downloads under the real Pages base path. Route authenticated user-only material to the appropriate access-controlled site or project when access differs.

**If users can create issues in the target project**, link to GitLab's new issue screen with the feature template selected. Confirm the link on the installed GitLab version. Create a label-backed intake column with the GitLab specialist when requested. Verify that a submitted test issue has the expected label and board visibility under the actual board filters. Use an approved test project or fixture for write verification.

**If users need an embedded form or lack GitLab project access**, agree on the submitter identity, moderation, and visibility first. Pages serves the UI. A separately hosted service validates submissions and creates an issue in a fixed project with approved labels. Keep GitLab credentials and any pipeline trigger token on the server side. Use bounded inputs, deduplication across retries, and an issue receipt. Add rate limits and spam controls appropriate to the audience. If processing needs CI, have the trusted service call a dedicated intake job with constrained inputs and check that the job identity can create the issue. Never accept a caller-selected destination or publish a token in the DocFX output.

Test navigation on a production-style path, then check valid, invalid, repeated and failed submissions. Count a successful submission only when the new issue can be read and appears in the intended board column.

[DocFX](https://dotnet.github.io/docfx/) · [GitLab Pages](https://docs.gitlab.com/user/project/pages/) · [GitLab issue templates](https://docs.gitlab.com/user/project/description_templates/) · [GitLab issues API](https://docs.gitlab.com/api/issues/)
