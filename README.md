# Codex for VS Code · C# and GitLab starter

Use the Codex extension in your existing VS Code workspace. The main chat orchestrates with **GPT-5.6 Terra / medium** and chooses specialized Terra or Luna roles for Inventor add-in development, GitLab CI, and the DocFX site. Keep your approved company provider configured on the machine where Codex runs. The desktop app can run a separate feature in its own managed Git worktree.

## Install in one repository

1. Clone this starter to a separate folder using the command below, then open the target application checkout in the VS Code environment where you run Codex.
2. Copy the TOML files from `repository/.codex/agents/` to `.codex/agents/` at the Git root. Merge any same-named role. Copy the three skill directories from `repository/.agents/skills/` to `.agents/skills/` at that same Git root. Codex discovers project skills at this location. [Local skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).
3. Merge `repository/.codex/config.toml` into the target repository's `.codex/config.toml`. Put root keys (`model`, `model_reasoning_effort`, `review_model`) before any TOML table. Merge existing `[agents]` and `[mcp_servers.openaiDeveloperDocs]` tables once. The starter allows four concurrent child threads, defaults unassigned agents to Luna / high, and connects the official documentation MCP server. Preserve your company provider and authentication in user-level configuration.
4. Merge `repository/AGENTS.md` with the repository's instructions. Replace the build-discovery paragraph with the exact commands from your CI or developer shell once you know them. Keep the Windows configuration/platform pair, restore method, adapter or runsettings, and any Inventor integration prerequisites together.
5. Optionally merge `personal/AGENTS.md` into your Codex home `AGENTS.md` for preferences that span projects. The normal home is `~/.codex` (usually `%USERPROFILE%\.codex` on native Windows). A VS Code session running Codex in WSL can use a different home and executable PATH. Project files travel with the checkout.
6. Install and review the [command protection hook](#protect-git-and-gitlab-commands).
7. Use a trusted project and open a fresh Codex chat at the repository root. In the **Codex sidebar**, run the smoke prompt below. Keep any organization-managed settings in force.

The configuration uses the current OpenAI names. Older managed clients that document only `max_threads` can use that key as the four-thread cap in place of `max_concurrent_threads_per_session`. The included `max_depth = 2` permits the planner-to-GitLab level on the V1 backend. V2 ignores that setting, so the orchestration instructions limit delegation to the intended roles. Agent dispatch also depends on the installed client and company policy. Check the Codex extension version deployed by your organization if the smoke prompt cannot find the roles. [Codex configuration schema](https://learn.chatgpt.com/docs/config-schema.json)

## VS Code and the desktop app

Keep VS Code as the main workspace for focused C# and XAML edits, editor selections, and reviewing diffs in place. Use your existing Windows build and Inventor environment for host checks. The extension already supports custom agents and skills. [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide) · [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

Use Codex in the ChatGPT desktop app when you want a separate chat and managed worktree for independent work such as DocFX navigation or a migration inventory. The desktop adds worktree setup scripts, reusable project actions, a Git review pane, and scheduled work. Use Handoff to bring an independent change back to the primary checkout for integration and live host checks. [Desktop worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) · [Desktop local environments](https://learn.chatgpt.com/docs/environments/local-environment).

On a Windows host with Inventor and Vault installed, use the native Windows agent for work that needs their SDKs or a live host. VS Code in WSL and the Windows-native desktop app may use different Codex homes and PATHs. Verify the provider, hooks, GitLab CLI, and Windows build command in the selected environment before relying on it. Worktrees isolate files, while installed Autodesk runtimes and add-in registration remain shared on that machine. [Windows desktop environments](https://learn.chatgpt.com/docs/windows/windows-app).

## Who owns what

| Role | Model | Reasoning | Assignment |
| --- | --- | --- | --- |
| Main chat | GPT-5.6 Terra | `medium` | Coordinate, reconcile, integrate, verify, and own the pass count |
| `planner` | GPT-5.6 Terra | `medium` | Translate request and repository facts into criteria, file owners, dependencies, and checks |
| `implementer` | GPT-5.6 Terra | `high` | Own one complete behavior slice and its ordinary tests |
| `dotnet_specialist` | GPT-5.6 Terra | `high` | Diagnose builds and interop, or plan Inventor and Vault runtime migration |
| `regression_reviewer` | GPT-5.6 Terra | `high` | Trace changed behavior through existing callers and report concrete regressions |
| `inventor_ipc_specialist` | GPT-5.6 Terra | `high` | Own the Windows named-pipe protocol, host-safe COM capture, and detached model snapshots |
| `desktop_ui_specialist` | GPT-5.6 Terra | `high` | Implement WPF add-in UI or evaluate WebView2 hosting and dependencies |
| `sqlite_specialist` | GPT-5.6 Terra | `high` | Own checklist schema, migrations, queries, and data preservation |
| `feature_intake_specialist` | GPT-5.6 Terra | `high` | Design or own the submission contract, identity, and issue creation path |
| `repo_mapper` | GPT-5.6 Luna | `high` | Answer one bounded code-path or test-coverage question |
| `gitlab_specialist` | GPT-5.6 Luna | `medium` | Update Kanban boards, inspect CI failures, and retry specific jobs or pipelines |
| `ci_pipeline_specialist` | GPT-5.6 Luna | `high` | Fix an assigned runner script or CI job using failure and artifact evidence |
| `pages_docs_specialist` | GPT-5.6 Luna | `high` | Own DocFX navigation, user and developer docs, releases, and suggestion UI |
| `test_engineer` | GPT-5.6 Luna | `high` | Implement focused fixtures and boundary cases for agreed behavior |
| `requirement_auditor` | GPT-5.6 Luna | `high` | Check each acceptance criterion against source and verification evidence |

Codex instructions describe how to delegate. They do not install a scheduler or isolate a role's credentials. The main chat names the requested roles and dispatches work. If nested dispatch is unavailable, the planner hands its GitLab lookup to the main chat, which sends the result back. Each included role pins both `model` and `model_reasoning_effort`; the table above is the intended policy. Custom agent files take precedence over explicit spawn settings, agent defaults, and parent settings. To change a pinned role, edit its TOML file and start a fresh chat. Set provider, MCP, approval, and sandbox controls on the parent session; custom roles inherit them.

## Model and reasoning choices

VoltAgent calls fixed per-role model selection **Smart Model Routing**. The starter already pins models in TOML and now records the task-to-role decision in project `AGENTS.md`. It adapts VoltAgent's API designer, .NET, frontend, DevOps, documentation, and test role patterns to this workflow. Codex uses `developer_instructions` for standalone role files and inherits permissions from the parent session, so the templates use the official schema and describe file ownership in the role instructions. [VoltAgent routing and example](https://github.com/VoltAgent/awesome-codex-subagents/blob/9abe3279a0aa4ee518381af800ca1062398f5433/README.md#smart-model-routing) · [Codex custom agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents).

These are project defaults for new chats after installation, not a change to an already running conversation. The IDE model picker, selected profile, or CLI overrides can supersede project defaults. Check the displayed root model and effort in a fresh chat. Root `review_model` also keeps the built-in `/review` on Terra; the custom `regression_reviewer` independently pins Terra / high.

Both GPT-5.6 model pages list `medium` as the default, and Codex describes it as balancing speed and depth. This starter keeps coordination and planning at medium, spends high effort on implementation and risky review, and gives Luna high for source tracing, tests, and acceptance checks. GitLab uses medium for explicit API operations. These role assignments are a practical recommendation, not an OpenAI-prescribed matrix. [Terra model](https://developers.openai.com/api/docs/models/gpt-5.6-terra), [Luna model](https://developers.openai.com/api/docs/models/gpt-5.6-luna), [Codex reasoning and agent settings](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning).

Luna assignments must stay bounded. Return architectural decisions, uncertain behavior across projects, and complex interop questions to the Terra orchestrator. The orchestrator can assign the work to a Terra role. A prompt asking a pinned Luna role to use Terra does not replace its file settings. Keep difficult fixture design with the implementer or .NET specialist; give the test engineer the agreed behavior and test-file ownership.

### Research on reasoning levels · checked 2026-11-22

There is no reliable community consensus establishing one best level for both models. The firsthand reports below are anecdotes and small experiments, not a representative survey or a benchmark of this .NET/Inventor workflow.

- One Codex user reports success with Terra / high for implementation and Luna / high for lookups and exploration. This supports high as a practical option for substantive delegated work, but the comment does not establish a universal ranking. [Reported setup](https://www.reddit.com/r/codex/comments/1vccxgh/we_need_another_25_off_terra/).
- Another early guide recommends Luna medium/high for tiny tasks, Luna xhigh for scoped fixes, and Terra medium for unclear work spanning a repository. Replies disagree about efficiency and favor different models. This supports choosing by scope and observed results. [Guide and discussion](https://www.reddit.com/r/codex/comments/1utzi5w/gpt56_sol_vs_terra_vs_luna_my_early_guide_to/).
- Users also report long reasoning and polishing cycles on ordinary tasks, including Luna and Terra. This is a workflow complaint, not a controlled comparison between effort settings. [Overthinking report](https://www.reddit.com/r/codex/comments/1us6on4/gpt56_is_burning_my_5hour_quota_by_overthinking/).
- An October 25 research preprint reports Terminal-Bench solve rates of 52.8%, 62.9%, and 70.8% for Luna medium/high/xhigh; Terra scored 68.5%, 74.2%, and 74.2%. Its corrected SWE-Bench sample was only 44 tasks and did not show uniform improvement at each step. These results support selective escalation, not an across-the-board xhigh default. Different harnesses and small samples limit transfer to Codex in this repository. [Study, Table 4 and methodology](https://borowiecki.dev/pdf/2610.34491).
- A firsthand single-brief web-design comparison found rendering defects did not improve monotonically with effort. Its initial-viewport checks do not measure repository maintenance or production readiness. [Experiment and artifacts](https://stranmor.com/research/gpt-5-6-reasoning-effort).

For this starter, use **medium for coordination and mechanical work, high for substantive coding or analysis**. Try xhigh only for a specific unresolved problem; record whether it improves the result. Compare completed-task time, repeated reads, failed attempts, and useful findings. The existing three-pass limit still applies. Higher effort alone does not control scope: give each role a stopping condition and stop when its assigned checks pass.

## Protect Git and GitLab commands

Copy `repository/.codex/hooks.json` and `repository/.codex/hooks/guard_commands.py` to the same paths under the target checkout's `.codex/` directory. If the project already has hooks, append this `PreToolUse` group to its existing hook configuration. Use a recent local Codex client and Python 3.9+ on the Codex host. The launcher uses `python3` on Linux, macOS and WSL, and `python` on native Windows with PowerShell. Start Codex in the trusted checkout, review the script, and use `/hooks` in the Codex CLI to trust the hook. Open a fresh VS Code chat after installing or changing it. [Codex hook setup and trust](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks).

| Allows in Codex | Requires manual execution |
| --- | --- |
| Status, diff, fetch, normal pushes and branch switches | Force pushes (including `--force-with-lease`), remote ref deletion, and mirror or prune pushes |
| `git clean -n` and `git restore --staged` | Hard resets, working tree restores, forced branch changes, non-dry-run cleans and stash deletion |
| GitLab REST `GET` and `HEAD`, including failed pipelines, job details and traces | GitLab `DELETE`, job erasure, cancellation, new pipeline runs, and manual job starts |
| Explicit REST writes to create or update project and group boards, lists and labels. Agents can create or update project issues and add comments | Other `glab api` writes, GraphQL, implicit POSTs, method overrides, and body files or multipart forms |
| Retry a specific job with `glab ci retry <job-id>` or REST `POST`. Retry failed or canceled jobs in a specific pipeline with REST `POST` | Interactive `glab ci view` and untargeted CLI retries. Use `glab ci get`, `glab ci trace`, or REST GET for inspection |
| Ordinary file cleanup | Direct recursive deletion or removal of `.git` metadata |

Verify activation from a Codex chat in a scratch checkout. Ask it to run `git status --short` and then `git -C missing-canary-path reset --hard`, using a directory name that does not exist. The first should run and the second should show the hook's denial before Git can report a missing directory. For a GitLab check, ask it to run `glab api --hostname example.invalid -X DELETE projects/0`. The hook should deny it before the CLI attempts a connection.

The hook inspects visible shell commands, including common shell wrappers and pipelines. Scripts, aliases, shell expansion, direct HTTP clients, MCP tools and manual terminal commands fall outside its coverage. Configure Git server branch protections and use read-scoped GitLab credentials for sessions that only need retrieval. When the hook blocks an intended write, ask Codex for the exact command and target so you can review and execute it yourself. [Codex hook tool coverage](https://learn.chatgpt.com/docs/hooks#tool-coverage).

## Configure GitLab

Use the official `glab` CLI on the host where Codex executes commands. Sign in to the company instance using your approved method. A credential with `read_api` scope and project access is enough for retrieval. Applied changes require an identity with write capability and the GitLab role required for the operation. A Codex role description alone cannot enforce that distinction. For technically enforced retrieval-only sessions, expose only a read-scoped identity to the session.

From the target checkout, replace the example hostname and run these checks in PowerShell. Use the ID of an existing board from the second response for the last command.

```powershell
$GitLabHost = 'gitlab.example.com'
glab auth login --hostname $GitLabHost
glab api --hostname $GitLabHost --method GET 'projects/:fullpath'
glab api --hostname $GitLabHost --method GET --paginate 'projects/:fullpath/boards'
$BoardId = Read-Host 'Existing project board ID'
glab api --hostname $GitLabHost --method GET --paginate "projects/:fullpath/boards/$BoardId/lists"
```

| Board task | REST API |
| --- | --- |
| Read a project board and its scope | `GET /projects/:id/boards/:board_id` |
| Retrieve a ticket and acceptance text | `GET /projects/:id/issues/:issue_iid` |
| List cards for a label-backed column | `GET /projects/:id/issues` with the applicable state, labels, board scope, and pagination |
| Create a project board for an authorized request | `POST /projects/:id/boards` |
| Update the board name or scope | `PUT /projects/:id/boards/:board_id` |
| Add a missing label-backed column | Find or create its project label, then `POST /projects/:id/boards/:board_id/lists` with the label ID |
| Reorder a board column | `PUT /projects/:id/boards/:board_id/lists/:list_id` with `position` |
| Move an issue between label lists | `PUT /projects/:id/issues/:issue_iid` using `remove_labels` and `add_labels` for that transition |

Group boards have their own API. The board-list response describes the columns. To reconstruct the cards, the agent also needs issues, board filters, and the rule for each column. The project lists endpoint omits the built-in Open and Closed lists. Check available features against your self-managed GitLab version and tier.

**Board design prompt**

> Use planner and gitlab_specialist to design a project board for this feature. Inspect existing boards, labels, and issue templates. Propose columns for Ready, In progress, and Review using our existing workflow labels where possible. Return the proposed board, reusable issue IIDs, missing labels and lists, and draft acceptance criteria. Proposal only.

**Board apply prompt**

> Apply the agreed board changes in the named project. Re-read the current board and create only what is missing. Preserve existing cards and unrelated labels. Verify the updated board and return the board URL, affected list IDs, and issue links.

Use `--method POST` or `--method PUT` and supply documented fields with `-f` or `-F`. The hook accepts numeric project or group IDs and URL-encoded paths such as `group%2Fproject`. Use concrete board, list, issue, job, and pipeline IDs in API writes. For a group board, update cards through each issue's owning project. [Project boards API](https://docs.gitlab.com/api/boards/) · [Group boards API](https://docs.gitlab.com/api/group_boards/) · [GLab API flags](https://docs.gitlab.com/cli/api/).

**Inspect and retry CI failures**

Read the failed jobs for the specific pipeline and fetch the relevant job trace. The following example uses project `42`, pipeline `123` and job `456`. Substitute the actual host and IDs before running it.

```powershell
glab api --hostname $GitLabHost --method GET --paginate -f 'scope[]=failed' 'projects/42/pipelines/123/jobs'
glab api --hostname $GitLabHost --method GET 'projects/42/jobs/456/trace'
glab api --hostname $GitLabHost --method POST 'projects/42/jobs/456/retry'
```

When a retry is requested, verify the job belongs to the selected pipeline and SHA, retry that job once, and check the new job ID and status. Use `POST projects/42/pipelines/123/retry` only when the request covers all failed or canceled jobs in that pipeline. Check whether the retry would run deployment or release work before proceeding. [Jobs API](https://docs.gitlab.com/api/jobs/) · [Pipelines API](https://docs.gitlab.com/api/pipelines/).

## Give the mapper C# symbols

If your existing Roslyn service already exposes definition and reference lookup to Codex, use it first. The mapper can also use search and focused file reads without a semantic service.

For an off-the-shelf option, Serena is an open-source local MCP server with a C# language-server backend. Its current default C# backend uses Roslyn and requires .NET 10+ and, on Windows, PowerShell 7+. These are tooling prerequisites. Keep the application targeted to .NET Framework 4.8. Run the server where it can load your actual solution and its references. For Inventor projects, start on the Windows side where your existing build resolves the Inventor assemblies.

1. Install the approved Serena distribution on the Codex host. Upstream currently documents `uv tool install -p 3.13 serena-agent` followed by `serena init`. For a managed host use your approved package source or pinned build. The C# server may download runtime components at first use.
2. From the solution checkout, run `serena project create --index` for a new project. Select C# when prompted. For an existing Serena project, run `serena project index`. This warms the symbol cache. Serena updates it during normal use.
3. Merge `optional/serena.toml` into the active Codex configuration and start a fresh thread. The executable must resolve from the Codex host. When VS Code runs Codex in WSL, a native Windows Serena setup needs a working launcher and the correct Windows solution path. Opening the checkout with native Windows Codex avoids that extra boundary.
4. Try a symbol with a known caller in a different project. Ask for the exact declaration, overload, and calling method. Compare that answer with the IDE's Find All References. Also trace one add-in command through its manifest or event wiring using targeted text search. Check solution-load diagnostics before relying on an empty reference set.

If you also maintain a RepoPilot catalog, use it for the durable project map and build profiles. Use Roslyn or Serena for current symbol identity and references. Let one mapper return just the paths, symbols, and context needed for the task.

## Inventor, Vault, and the add-in UI

Keep the Inventor 2024 package on .NET Framework 4.8 while you support that host. Inventor 2025 moved to .NET 8, and older 2026 builds were from that runtime generation. Autodesk's updated Inventor 2026.4 and Vault 2026.4 move to .NET 10. Microsoft ended .NET 8 support on November 10, 2026. For an updated 2026.4 deployment, start with `net10.0-windows` and verify matching Autodesk SDKs, dependencies and deployment on the exact Inventor/Vault images. If both generations remain in use, plan separate host-specific packages and keep the pipe and snapshot contract compatible. [Autodesk transition guidance](https://help.autodesk.com/view/INVNTOR/2026/ENU/?caas=caas%2Fsfdcarticles%2Fsfdcarticles%2FInventor--Requirements-for-products-affected-by-the-Microsoft--NET-10-transition.html) · [Vault 2026.4 runtime](https://help.autodesk.com/cloudhelp/2026/ENU/Vault-New/files/WN-general-2026_4.htm) · [Microsoft lifecycle](https://learn.microsoft.com/en-us/lifecycle/products/microsoft-net-and-net-core).

Keep the WPF shell through the migration. A toolkit upgrade should address a specific compatibility gap or UI requirement. Check the exact package and version on both targets before choosing an upgrade. Use WebView2 for specific web content when it earns the extra runtime and bridge work. Test its installed runtime, window lifetime, keyboard behavior, and allowed origins inside Inventor. [WPF migration](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/migration/) · [WebView2 for WPF](https://learn.microsoft.com/en-us/microsoft-edge/webview2/get-started/wpf) · [WebView2 security](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/security).

Use `sqlite_specialist` when a checklist change affects saved data, schema compatibility, or database performance. One owner keeps migration SQL and its callers aligned. Verify upgrades against a disposable database from a supported older release using the SQLite provider shipped with the add-in. Keep ordinary UI edits with the current implementer. [SQLite schema changes](https://sqlite.org/lang_altertable.html) · [SQLite foreign keys](https://sqlite.org/foreignkeys.html).

## DocFX Pages and feature suggestions

Keep the existing DocFX build. Give users clear links to usage guides, releases, and feature suggestions. Give developers a separate navigation path to API and development docs. If those audiences require different access, use separate access-controlled projects or sites. Verify navigation and downloads under the actual Pages path before publishing. [DocFX documentation](https://dotnet.github.io/docfx/) · [Pages access control](https://docs.gitlab.com/user/project/pages/pages_access_control/).

1. If submitters can create GitLab issues, start with a link to the new issue page with a feature proposal template selected. Apply the intake label and verify the resulting ticket matches the Kanban column and any board filters. This path uses GitLab's own sign-in and issue submission flow. [Issue links and prefills](https://docs.gitlab.com/user/project/issues/create_issues/) · [Description templates](https://docs.gitlab.com/user/project/description_templates/).
2. If users need an embedded form or lack GitLab access, host an intake endpoint separately. Have it validate and deduplicate submissions, authenticate callers or moderate abuse as appropriate, create the issue in a fixed project, and return a receipt. Keep GitLab credentials server-side. Route through a dedicated pipeline only if intake needs async processing or mediation and the service and job identities have the necessary access. GitLab Pages serves static files. [GitLab Pages](https://docs.gitlab.com/user/project/pages/) · [Issues API](https://docs.gitlab.com/api/issues/) · [Pipeline triggers](https://docs.gitlab.com/ci/triggers/).

## Optional tools

| Tool | Use in this workflow |
| --- | --- |
| Microsoft Learn MCP | Merge [optional/microsoft-learn.toml](optional/microsoft-learn.toml) for .NET, WPF, WebView2 and Windows API references. Confirm the optional server is usable on the approved Codex host. [Microsoft endpoint](https://learn.microsoft.com/en-us/training/support/mcp) |
| Roslyn or Serena | Use the approved Windows-host symbol service for source lookup and references. Use the installed Inventor and Vault SDKs and sample projects for Autodesk signatures. [Vault developer tools](https://help.autodesk.com/cloudhelp/Help/ENU/Vault/files/GUID-F21E7DD6-39E9-473C-84BB-3446BCAFCCC0.htm) |
| Playwright CLI or MCP | Use an approved, pinned tool version for local DocFX/Pages navigation, forms and release links. Run real WPF, WebView2-in-Inventor and COM checks on Windows. [Playwright CLI](https://github.com/microsoft/playwright-cli) · [Playwright MCP](https://github.com/microsoft/playwright-mcp) |
| GitLab MCP | Consider it for read-only issue and pipeline evidence if enabled on your GitLab instance. Check its available toolsets and permissions. Keep board writes and targeted retries on the guarded `glab` path. [GitLab MCP toolsets](https://docs.gitlab.com/user/model_context_protocol/mcp_server_tools/) |

The starter keeps these integrations optional. The installed project skills cover the workflow without adding a runtime service to the add-in or site.

## First delegated run

**Verify role discovery**

First confirm the root picker shows GPT-5.6 Terra / medium. Confirm the role files and documentation MCP server are loaded; a role repeating its model name is not proof of the actual backend model. Inspect available thread metadata or provider request logs when your client exposes them.

> Use the custom repo_mapper and requirement_auditor roles. Ask the mapper to identify the real Windows build and MSTest commands from this repository. Ask the auditor to independently identify the evidence required for an Inventor-hosted acceptance check. Show each role's returned result. Inspection only.

**Run a feature**

> Orchestrate GitLab issue #123 using the delegated workflow in AGENTS.md. Use the smallest useful set of agents from its routing table. Verify the Windows build, managed tests, and any required Inventor host checks. Review the integrated changes independently against the original issue. Leave GitLab unchanged for this run.

**Plan the 2026 migration**

> Use $inventor-runtime-migration and the dotnet_specialist. Inventory the 2024 package and the exact 2026 Inventor and Vault versions we plan to deploy. Return a runtime and packaging matrix, dependency gaps, and a Windows verification plan. Planning only.

**Plan feature intake**

> Use $gitlab-pages-intake. Have pages_docs_specialist inspect our DocFX routes and feature_intake_specialist verify whether our intended users can submit to the destination project. Propose a user/developer navigation split and a feature submission path. Show how one issue would reach the intended board column. Proposal only.

For a small change, one implementer can own both the fix and its test. Add the testing agent when a prior version should demonstrate a failure, several input states produce different outcomes, or a fixture needs expertise. For example, the implementer can wire an Inventor command while the testing agent characterizes an existing filename-mapping rule used by that command. Reserve a live Inventor check for loading the add-in and invoking the command.

## Fill in repository-specific facts

Replace these examples in your repository guidance with the exact commands that already work for your developers or CI. Keep any `packages.config` restore step, adapter path, or `.runsettings` file your repository uses.

```powershell
# From the Visual Studio Developer PowerShell used by this repository
MSBuild.exe 'YourSolution.sln' /t:Build /m /p:Configuration=Debug '/p:Platform=Any CPU'
vstest.console.exe 'path\to\Your.Tests.dll' /Logger:trx
```

Specify one small fixture for a live check, the Inventor command to invoke, and what the tester should observe. During a feature run, keep a short table in the primary chat with acceptance ID, current status, file or symbol, and executed check. Report discovery separately from a successful process exit. Track three things on your first few tickets: duplicated file reads, findings caught by only one reviewer, and wall time spent waiting for workers. Those observations will tell you whether another role would earn its cost.

## Get this starter at work

```powershell
git clone https://github.com/Ryan-Thornton-CS/codex-dotnet-gitlab-starter.git
```

The clone is a template collection. Install the files into your application checkout using the steps above. Configuration under `repository/.codex/` is inactive while you work at this starter's root. Authenticate GitLab and configure your approved model provider separately on the work machine; credentials are not part of the starter. Pull this starter when you want updated templates, then merge changes into the application checkout.

## Documentation

- [Codex agents / custom agent files and precedence](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) · [Agent defaults and thread limits](https://learn.chatgpt.com/docs/agent-configuration/subagents#global-settings) · [Reasoning levels](https://learn.chatgpt.com/docs/agent-configuration/subagents#reasoning-effort-model_reasoning_effort)
- [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) · [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) · [OpenAI documentation MCP](https://developers.openai.com/resources/docs-mcp)
- [Codex IDE extension](https://learn.chatgpt.com/docs/codex/ide) · [Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Desktop worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees)
- [AGENTS.md lookup](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Config precedence](https://learn.chatgpt.com/docs/config-file/config-basic) · [Config reference](https://learn.chatgpt.com/docs/config-file/config-reference) · [Advanced configuration](https://learn.chatgpt.com/docs/config-file/config-advanced) · [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [GitLab CLI API](https://docs.gitlab.com/cli/api/) · [Project boards API](https://docs.gitlab.com/api/boards/) · [Group boards API](https://docs.gitlab.com/api/group_boards/) · [Issues](https://docs.gitlab.com/api/issues/) · [Labels](https://docs.gitlab.com/api/labels/) · [Token scopes](https://docs.gitlab.com/security/tokens/access_token_scopes/)
- [Serena](https://github.com/oraios/serena) · [Installation](https://oraios.github.io/serena/02-usage/010_installation.html) · [Language support](https://github.com/oraios/serena/blob/main/docs/01-about/020_programming-languages.md) · [Project indexing](https://oraios.github.io/serena/02-usage/040_workflow.html) · [Codex connection](https://oraios.github.io/serena/02-usage/030_clients.html)
- [MSBuild command line](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-command-line-reference) · [VSTest console](https://learn.microsoft.com/en-us/visualstudio/test/vstest-console-options)
