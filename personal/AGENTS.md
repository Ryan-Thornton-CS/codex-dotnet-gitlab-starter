# Personal working preferences

For feature work I ask you to delegate, let the primary chat coordinate the work. Delegate independent tasks, keep the packets small, and return decisions to the primary chat. Match the amount of planning to the scope of the change.

Use at most three implementation-and-review passes per feature unless I explicitly extend the limit. Stop as soon as the acceptance criteria and relevant checks are satisfied. At handoff, show what passed, what remains open, and any environment-dependent checks I still need to run.

Use each repository's documented build commands, test commands, toolchain, and house conventions. Preserve unrelated work in progress.

Honor the repository's configured role/model policy. For this starter, Terra owns coordination, planning, substantive implementation, interop diagnosis, and regression review; Luna handles bounded mapping, GitLab operations, focused tests, and acceptance checks. Use the role's configured effort and escalate a specific unresolved question instead of automatically choosing maximum reasoning. Keep these model preferences in the relevant TOML configuration; prose alone does not select a backend model.
