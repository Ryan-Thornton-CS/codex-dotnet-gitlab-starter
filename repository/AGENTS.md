# Working in this repository

## Toolchain and verification

This repository targets C# on .NET Framework 4.8 and integrates with Autodesk Inventor 2024. Use the repository's existing MSBuild and MSTest workflow on the Windows build host. Identify the actual solution, configuration, platform, package restore method, test assembly, and adapter from the checked-in scripts and CI. Follow the existing language version and project-file conventions.

Keep operations that require Inventor separate from tests of ordinary .NET behavior. Record the host used, exact command, result, and number of tests executed. If the runner discovers zero tests, investigate discovery. If the required host is unavailable, identify exactly which checks are still open.

## Model and reasoning policy

The project configuration defaults the main chat to GPT-5.6 Terra / medium and unassigned subagents to GPT-5.6 Luna / high. The custom TOML files are authoritative for each role: planner uses Terra / medium; implementer, dotnet_specialist, and regression_reviewer use Terra / high; repo_mapper, test_engineer, and requirement_auditor use Luna / high; gitlab_specialist uses Luna / medium.

Keep Luna assignments narrow and evidence-based. Send architectural choices, complex fixture design, uncertain behavior across projects, and COM or host reasoning to the main chat for a Terra assignment. A role's pinned settings take precedence over a spawn-time model request; use the appropriate Terra role rather than trying to override a Luna role in its task prompt. Do not repeatedly raise effort on a vague assignment. Clarify its observable result and stopping condition first.

For Codex configuration questions, use the configured `openaiDeveloperDocs` MCP server and official documentation. [Custom agents and settings](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md) · [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## Delegated feature work

The main Codex conversation owns the feature from request through verification. Apply the following workflow when the user requests delegated feature work. Handle a narrow question or a one-file change directly when appropriate. An agent receiving one assignment follows its own role and returns findings to its caller.

1. Capture the request, its source, and any acceptance criteria. In parallel, send `repo_mapper` one code question and `planner` the feature request. Add a second mapper only for a distinct question, such as affected integration points or test coverage. Request paths, symbols, and evidence.
2. For GitLab work, the planner may delegate a single lookup or explicitly authorized board change to `gitlab_specialist`. If the planner cannot spawn a child, have it return its question. The primary chat can dispatch that specialist and pass the results back. Other roles complete their own assignments.
3. Give the planner the repository findings before finalizing the plan. The main chat reconciles ambiguities, numbers the acceptance criteria, and records ownership and validation for each slice. Preserve the request independently so reviewers can spot requirements the plan omitted.
4. Give each `implementer` an end-to-end behavior or a disjoint set of files, acceptance IDs, expected caller behavior, and a verification command. Assign shared files such as a legacy .csproj or solution file to one owner. Sequence dependent edits. Add `dotnet_specialist` for framework, build, or interop risks. Use `test_engineer` when the testing work warrants separate ownership.
5. After edits are integrated and writers have stopped, run the applicable build and tests against the combined working tree. Serialize builds that share output directories. Send `requirement_auditor` and `regression_reviewer` the original request, acceptance IDs, base revision, current changes (including new files), and actual test results. Run both reviews in parallel. Reviewers report findings without changing code.
6. Count the first integrated implementation and its two reviews as pass 1. Correct supported findings and rerun affected checks before the next review. Stop early when all required criteria have evidence and material findings are resolved. Stop after pass 3 with any remaining gaps and unverified checks listed. Use a fourth pass only at the user's request.

Keep the task ledger in the main chat. It needs only the acceptance IDs, owners, evidence, outstanding findings, and current pass. Report each material finding with the affected caller or requirement, file and symbol, and a way to check it.
