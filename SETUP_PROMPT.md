# Install the Codex starter in this application repository

Use this file as a prompt in a Codex chat opened at the application repository you want to set up. If you have both repositories locally, tell Codex where the starter checkout is. Otherwise it can fetch the public starter from GitHub.

## Assignment

Install the project-scoped Codex configuration from `Ryan-Thornton-CS/codex-dotnet-gitlab-starter` into the application checkout open in this chat. Make the local file changes and verify them. Use that checkout's existing development and CI conventions as the source of truth.

## Identify the target and source

1. Find the target Git root with `git rev-parse --show-toplevel`. Read its applicable `AGENTS.md` files and inspect `git status --short --branch` before editing. Preserve existing changes. If the current folder is the starter itself or the target is ambiguous, get the application checkout path before writing.
2. Use the starter checkout I provide. If I provide a revision, read the templates at that revision. If I provide no checkout, clone `https://github.com/Ryan-Thornton-CS/codex-dotnet-gitlab-starter.git` into a temporary directory outside the target and use the requested revision or the default branch. Record the source commit SHA. Read the starter README and install from its `repository/` directory.
3. Identify whether Codex commands run in native Windows or WSL and whether Git, Python 3.9+, `glab`, and the Windows build tools are available on the relevant host. Report missing tools and continue with the file setup where possible. Keep credential and machine setup with the existing approved work environment.

## Merge the project files

| Source in the starter | Destination at the application Git root |
| --- | --- |
| `repository/AGENTS.md` | `AGENTS.md` |
| `repository/.codex/config.toml` | `.codex/config.toml` |
| `repository/.codex/agents/` | `.codex/agents/` |
| `repository/.codex/hooks.json` | `.codex/hooks.json` or the existing project hook configuration |
| `repository/.codex/hooks/guard_commands.py` | `.codex/hooks/guard_commands.py` |
| `repository/.agents/skills/` | `.agents/skills/` |

- Merge `AGENTS.md` into existing instructions. Keep the target's actual C#, Inventor, and Vault versions. Find the documented restore, build, and test commands in CI and local scripts. Record the Windows shell, solution, configuration, platform, runner, and any MSTest adapter or runsettings you can verify. Leave unknowns explicit. Keep the routing and GitLab rules relevant to this repo.
- Merge TOML keys into their existing tables. Put `model`, `model_reasoning_effort`, and `review_model` at the top level. Apply the starter's Terra/Luna model defaults and role settings where compatible with the work provider and managed policy. Preserve established authentication, provider, and unrelated MCP settings. Report any incompatible model or setting with the exact location and effect. Keep the supplied defaults if availability just needs a fresh-chat check.
- Copy every role file and every complete skill directory, including supporting resources and licenses. Merge same-name roles deliberately. Preserve a differing same-name skill or hook implementation and report what needs reconciliation. Keep installed role names aligned with references in `AGENTS.md`.
- Add the guard once. If the project already defines hooks inline under `[hooks]` in `.codex/config.toml`, merge there. If it uses `.codex/hooks.json`, merge into that file. Preserve other handlers and both platform launchers. Keep Codex's normal hook review and trust process in place.
- Install the project files only. Add optional Microsoft Learn or Serena settings, or merge the personal `AGENTS.md`, only if I requested that option. Keep this setup in the working tree for review. Treat commits, pushes, GitLab writes, pipeline actions, and application or CI changes as separate requests.

## Verify and hand off

1. Parse the installed TOML and hook JSON if used. Check that each expected role has its model, reasoning effort, description, and `developer_instructions`. Check that each skill has `SKILL.md` at the installed path. Confirm that exactly one hook calls the existing guard file, the launcher matches the host, and a second setup pass would avoid duplicate tables, roles, skills, and handlers.
2. Test the installed guard directly with synthetic `PreToolUse` JSON. Check that it permits `git status --short`, a GitLab trace read, a board write with explicit fields, and a targeted retry. Check that it rejects a hard reset, a GitLab DELETE, and job erasure. Feed the strings to the guard and inspect its result. These commands are test data.
3. Check client discovery where available. Separate files verified on disk, skills or roles discovered by Codex, and any agent execution you actually observed. Configuration installed during this chat may require a new chat. If the hook is awaiting review, tell me to inspect and trust it with `/hooks` in the intended checkout. Record live hook activation as pending until a fresh session demonstrates it. Follow the starter README's [scratch smoke check](README.md#protect-git-and-gitlab-commands).
4. Review the target diff and status. Report the target root, source SHA, files merged, installed roles and skills, verified build and test commands, checks passed, and any conflicts or host-dependent checks still open. Give me a short smoke prompt for a fresh chat that asks `repo_mapper` to confirm the real build/test entry points and `requirement_auditor` to list the Inventor host checks. Use inspection only for that smoke test.
