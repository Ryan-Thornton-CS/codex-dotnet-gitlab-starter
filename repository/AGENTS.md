# Working in this repository

## Toolchain and verification

This repository targets C# on .NET Framework 4.8 and integrates with Autodesk Inventor 2024. Use the repository's existing MSBuild and MSTest workflow on the Windows build host. Identify the actual solution, configuration, platform, package restore method, test assembly, and adapter from the checked-in scripts and CI. Follow the existing language version and project-file conventions.

Keep the current Inventor 2024 target for ordinary work. For an authorized migration, establish the exact Inventor and Vault updates, runtime targets and deployed artifacts before changing project files.

Keep operations that require Inventor separate from tests of ordinary .NET behavior. Record the host used, exact command, result, and number of tests executed. If the runner discovers zero tests, investigate discovery. If the required host is unavailable, identify exactly which checks are still open.

## Project skills

Use the skills under `.agents/skills/` for these tasks. Load only the references needed for the current assignment.

| Skill | Use it when |
| --- | --- |
| [`inventor-host-work`](.agents/skills/inventor-host-work/SKILL.md) | The change crosses Inventor COM, named pipes, model snapshots, or add-in UI |
| [`inventor-runtime-migration`](.agents/skills/inventor-runtime-migration/SKILL.md) | Moving to a different Inventor or Vault runtime or package |
| [`gitlab-pages-intake`](.agents/skills/gitlab-pages-intake/SKILL.md) | Updating DocFX Pages, feature suggestions, or the path from submission to a board card |
| [`playwright`](.agents/skills/playwright/SKILL.md) | Exercising a Pages preview in a real browser, including links, navigation and form behavior |
| [`aspnet-core`](.agents/skills/aspnet-core/SKILL.md) | Designing or implementing a separately hosted ASP.NET Core intake service using an agreed target framework |
| [`security-threat-model`](.agents/skills/security-threat-model/SKILL.md) | The user explicitly requests threat modeling for the intake endpoint, named-pipe trust boundary, or WebView2 bridge |

For Playwright, use the approved CLI on the Codex host. Resolve any bundled wrapper from the project skill at `.agents/skills/playwright/scripts/playwright_cli.sh`. Exercise forms against a local preview or test destination. Use the Windows Inventor host to check WPF and embedded WebView2 behavior. Keep the existing GitLab authorization and hook rules for live actions.

## Model and reasoning policy

The project configuration defaults the main chat to GPT-5.6 Terra at medium and unassigned subagents to GPT-5.6 Luna at high. The custom TOML files define each role's settings. Choose by task scope, uncertainty and consequences, and use the smallest useful set of roles.

| Work | Route |
| --- | --- |
| Planning, implementation, migration or regression reasoning | Terra `planner`, `implementer`, `dotnet_specialist`, or `regression_reviewer` |
| Named-pipe protocol, Inventor COM capture or in-memory snapshots | Terra `inventor_ipc_specialist` |
| WPF, WebView2 or add-in window behavior | Terra `desktop_ui_specialist` |
| SQLite checklist schema, migrations, query performance or persistence defects | Terra `sqlite_specialist` |
| Feature intake trust, backend, CI trigger design or issue creation contract | Terra `feature_intake_specialist` |
| Bounded tracing, MSTest fixtures or acceptance evidence | Luna `repo_mapper`, `test_engineer`, or `requirement_auditor` |
| Live board actions, pipeline evidence or targeted retries | Luna `gitlab_specialist` |
| Checked-in CI YAML or runner scripts | Luna `ci_pipeline_specialist`. Send cross-runner or release design decisions to Terra |
| DocFX navigation, user guides, release pages or suggestion UI | Luna `pages_docs_specialist`. Send backend and access decisions to Terra |

Keep Luna assignments narrow and evidence-based. Send architectural choices, complex fixture design, uncertain behavior across projects, and COM or host reasoning to the main chat for a Terra assignment. A role's pinned settings take precedence over a spawn-time model request; use the appropriate Terra role rather than trying to override a Luna role in its task prompt. Do not repeatedly raise effort on a vague assignment. Clarify its observable result and stopping condition first.

Keep routine checklist UI changes with their assigned implementer. Bring in `sqlite_specialist` when work changes persisted data or the database contract, or when it needs SQLite-specific diagnosis. Give one owner the schema, migration, and affected queries. Test upgrades on a disposable database from a supported older release.

For Codex configuration questions, use the configured `openaiDeveloperDocs` MCP server and official documentation. [Custom agents and settings](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

For an authorized GitLab board change, verify the target, apply the smallest allowed update, and re-read the affected resources. Inspect CI failures by project, pipeline, SHA, and job ID. Retry the specific job when requested and use a pipeline retry only when the requested scope covers its failed or canceled jobs. If the command protection hook denies an operation, preserve that decision and report the exact target and proposed operation for manual review.

## Delegated feature work

The main Codex conversation owns the feature from request through verification. Apply the following workflow when the user requests delegated feature work. Handle a narrow question or a one-file change directly when appropriate. An agent receiving one assignment follows its own role and returns findings to its caller.

1. Capture the request, its source, and any acceptance criteria. In parallel, send `repo_mapper` one code question and `planner` the feature request. Add a second mapper only for a distinct question, such as affected integration points or test coverage. Request paths, symbols, and evidence.
2. For GitLab work, the planner may delegate a single lookup or explicitly authorized board change to `gitlab_specialist`. If the planner cannot spawn a child, have it return its question. The primary chat can dispatch that specialist and pass the results back. Other roles complete their own assignments.
3. Give the planner the repository findings before finalizing the plan. The main chat reconciles ambiguities, numbers the acceptance criteria, and records ownership and validation for each slice. Preserve the request independently so reviewers can spot requirements the plan omitted.
4. Give each writer an end-to-end behavior or a disjoint set of files, acceptance IDs, expected caller behavior, and a verification command. Choose the specialist whose files and responsibility match the slice. Assign shared `.csproj`, CI YAML, DTOs, or submission contracts to one owner. Set a shared contract before dispatching dependent work. Use `test_engineer` when the testing work warrants separate ownership.
5. After edits are integrated and writers have stopped, run the applicable build and tests against the combined working tree. Serialize builds that share output directories. Send `requirement_auditor` and `regression_reviewer` the original request, acceptance IDs, base revision, current changes (including new files), and actual test results. Run both reviews in parallel. Reviewers report findings without changing code.
6. Count the first integrated implementation and its two reviews as pass 1. Correct supported findings and rerun affected checks before the next review. Stop early when all required criteria have evidence and material findings are resolved. Stop after pass 3 with any remaining gaps and unverified checks listed. Use a fourth pass only at the user's request.

Keep the task ledger in the main chat. It needs only the acceptance IDs, owners, evidence, outstanding findings, and current pass. Report each material finding with the affected caller or requirement, file and symbol, and a way to check it.
