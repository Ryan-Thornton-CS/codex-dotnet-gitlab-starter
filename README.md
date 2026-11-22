# Codex for VS Code · C# and GitLab starter

Use the Codex extension in your existing VS Code workspace. The main chat orchestrates with **GPT-5.6 Terra / medium**. Eight custom roles use Terra or Luna with explicit reasoning settings matched to their work. Keep your approved company provider configured on the machine where Codex runs. The desktop app becomes useful when you want a second independent feature running in its own managed Git worktree.

## Install in one repository

1. Clone this starter to a separate folder using the command below, then open the target application checkout in the VS Code environment where you run Codex.
2. Copy the eight TOML files from `repository/.codex/agents/` to `.codex/agents/` at the Git root. Merge any same-named role with your existing definition.
3. Merge `repository/.codex/config.toml` into the target repository's `.codex/config.toml`. Put root keys (`model`, `model_reasoning_effort`, `review_model`) before any TOML table. Merge existing `[agents]` and `[mcp_servers.openaiDeveloperDocs]` tables once. The starter allows four concurrent child threads, defaults unassigned agents to Luna / high, and connects the official documentation MCP server. Preserve your company provider and authentication in user-level configuration.
4. Merge `repository/AGENTS.md` with the repository's instructions. Replace the build-discovery paragraph with the exact commands from your CI or developer shell once you know them. Keep the Windows configuration/platform pair, restore method, adapter or runsettings, and any Inventor integration prerequisites together.
5. Optionally merge `personal/AGENTS.md` into your Codex home `AGENTS.md` for preferences that span projects. The normal home is `~/.codex` (usually `%USERPROFILE%\.codex` on native Windows). A VS Code session running Codex in WSL can use a different home and executable PATH. Project files travel with the checkout.
6. Install and review the [command protection hook](#protect-git-and-gitlab-commands).
7. Use a trusted project and open a fresh Codex chat at the repository root. In the **Codex sidebar**, run the smoke prompt below. Keep any organization-managed settings in force.

The configuration uses the current OpenAI names. Older managed clients that document only `max_threads` can use that key as the four-thread cap in place of `max_concurrent_threads_per_session`. The included `max_depth = 2` permits the planner-to-GitLab level on the V1 backend. V2 ignores that setting, so the orchestration instructions limit delegation to the intended roles. Agent dispatch also depends on the installed client and company policy. Check the Codex extension version deployed by your organization if the smoke prompt cannot find the roles. [Codex configuration schema](https://learn.chatgpt.com/docs/config-schema.json)

## Who owns what

| Role | Model | Reasoning | Assignment |
| --- | --- | --- | --- |
| Main chat | GPT-5.6 Terra | `medium` | Coordinate, reconcile, integrate, verify, and own the pass count |
| `planner` | GPT-5.6 Terra | `medium` | Translate request and repository facts into criteria, file owners, dependencies, and checks |
| `implementer` | GPT-5.6 Terra | `high` | Own one complete behavior slice and its ordinary tests |
| `dotnet_specialist` | GPT-5.6 Terra | `high` | Diagnose legacy builds, COM, Inventor, and test discovery |
| `regression_reviewer` | GPT-5.6 Terra | `high` | Trace changed behavior through existing callers and report concrete regressions |
| `repo_mapper` | GPT-5.6 Luna | `high` | Answer one bounded code-path or test-coverage question |
| `gitlab_specialist` | GPT-5.6 Luna | `medium` | Retrieve tickets/boards or apply a specified board/label/issue transition |
| `test_engineer` | GPT-5.6 Luna | `high` | Implement focused fixtures and boundary cases for agreed behavior |
| `requirement_auditor` | GPT-5.6 Luna | `high` | Check each acceptance criterion against source and verification evidence |

Codex instructions describe how to delegate. They do not install a scheduler or isolate a role's credentials. The main chat names the requested roles and dispatches work. If nested dispatch is unavailable, the planner hands its GitLab lookup to the main chat, which sends the result back. Each included role pins both `model` and `model_reasoning_effort`; the table above is the intended policy. Custom agent files take precedence over explicit spawn settings, agent defaults, and parent settings. To change a pinned role, edit its TOML file and start a fresh chat. Set provider, MCP, approval, and sandbox controls on the parent session; custom roles inherit them.

## Model and reasoning choices

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
| GitLab REST `GET` and `HEAD`, including pagination and explicitly read-only query fields | GitLab API writes, implicit POSTs from fields, request bodies and GraphQL. The hook also blocks direct `glab` delete, remove, archive, transfer and revoke commands |
| Ordinary file cleanup | Direct recursive deletion or removal of `.git` metadata |

Verify activation from a Codex chat in a scratch checkout. Ask it to run `git status --short` and then `git -C missing-canary-path reset --hard`, using a directory name that does not exist. The first should run and the second should show the hook's denial before Git can report a missing directory. For a GitLab check, ask it to run `glab api --hostname example.invalid -X DELETE projects/0`. The hook should deny it before the CLI attempts a connection.

The hook inspects visible shell commands, including common shell wrappers and pipelines. Scripts, aliases, shell expansion, direct HTTP clients, MCP tools and manual terminal commands fall outside its coverage. Configure Git server branch protections and use read-scoped GitLab credentials where you need enforcement independent of Codex. When the hook blocks an intended write, ask Codex for the exact command and target so you can review and execute it yourself. [Codex hook tool coverage](https://learn.chatgpt.com/docs/hooks#tool-coverage).

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
| Add a missing label-backed column | Find or create its project label, then `POST /projects/:id/boards/:board_id/lists` with the label ID |
| Move an issue between label lists | `PUT /projects/:id/issues/:issue_iid` using `remove_labels` and `add_labels` for that transition |

Group boards have their own API. The board-list response describes the columns. To reconstruct the cards, the agent also needs issues, board filters, and the rule for each column. The project lists endpoint omits the built-in Open and Closed lists. Check available features against your self-managed GitLab version and tier.

**Board design prompt**

> Use planner and gitlab_specialist to design a project board for this feature. Inspect existing boards, labels, and issue templates. Propose columns for Ready, In progress, and Review using our existing workflow labels where possible. Return the proposed board, reusable issue IIDs, missing labels and lists, and draft acceptance criteria. Proposal only.

**Board change handoff prompt**

> Re-read the named project's current board and prepare the exact GitLab commands for the agreed changes. Include the host, project, dependent IDs and verification GETs. Preserve existing cards and unrelated labels. I'll run the writes in my terminal, then ask you to verify the resulting board and issue links.

## Give the mapper C# symbols

If your existing Roslyn service already exposes definition and reference lookup to Codex, use it first. The mapper can also use search and focused file reads without a semantic service.

For an off-the-shelf option, Serena is an open-source local MCP server with a C# language-server backend. Its current default C# backend uses Roslyn and requires .NET 10+ and, on Windows, PowerShell 7+. These are tooling prerequisites. Keep the application targeted to .NET Framework 4.8. Run the server where it can load your actual solution and its references. For Inventor projects, start on the Windows side where your existing build resolves the Inventor assemblies.

1. Install the approved Serena distribution on the Codex host. Upstream currently documents `uv tool install -p 3.13 serena-agent` followed by `serena init`. For a managed host use your approved package source or pinned build. The C# server may download runtime components at first use.
2. From the solution checkout, run `serena project create --index` for a new project. Select C# when prompted. For an existing Serena project, run `serena project index`. This warms the symbol cache. Serena updates it during normal use.
3. Merge `optional/serena.toml` into the active Codex configuration and start a fresh thread. The executable must resolve from the Codex host. When VS Code runs Codex in WSL, a native Windows Serena setup needs a working launcher and the correct Windows solution path. Opening the checkout with native Windows Codex avoids that extra boundary.
4. Try a symbol with a known caller in a different project. Ask for the exact declaration, overload, and calling method. Compare that answer with the IDE's Find All References. Also trace one add-in command through its manifest or event wiring using targeted text search. Check solution-load diagnostics before relying on an empty reference set.

If you also maintain a RepoPilot catalog, use it for the durable project map and build profiles. Use Roslyn or Serena for current symbol identity and references. Let one mapper return just the paths, symbols, and context needed for the task.

## First delegated run

**Verify role discovery**

First confirm the root picker shows GPT-5.6 Terra / medium. Confirm the role files and documentation MCP server are loaded; a role repeating its model name is not proof of the actual backend model. Inspect available thread metadata or provider request logs when your client exposes them.

> Use the custom repo_mapper and requirement_auditor roles. Ask the mapper to identify the real Windows build and MSTest commands from this repository. Ask the auditor to independently identify the evidence required for an Inventor-hosted acceptance check. Show each role's returned result. Inspection only.

**Run a feature**

> Orchestrate GitLab issue #123 in this repository using the custom agents. Start repo_mapper and planner in parallel. Have planner delegate the issue and board lookup to gitlab_specialist, or dispatch that lookup from the main chat if needed. Freeze the acceptance criteria after reconciling both reports. Delegate disjoint implementation slices. Add test_engineer or dotnet_specialist where useful. Build and run the relevant tests on the integrated changes, then run requirement_auditor and regression_reviewer independently. Stop at the first verified pass, with a maximum of three. Leave GitLab unchanged for this run.

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
