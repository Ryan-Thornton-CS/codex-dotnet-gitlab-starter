# Maintaining this starter

This repository contains reusable Codex configuration and instruction templates. It does not contain the .NET application described by `repository/AGENTS.md`; those application instructions apply when the templates are installed in a target checkout.

Keep model and reasoning settings in TOML, and keep the README role table consistent with all eight custom agent files. Preserve the requested GPT-5.6 Terra/Luna split. Verify configuration changes against the official Codex custom-agent and configuration documentation linked in README.md. Do not add machine-specific provider endpoints, credentials, or authentication state.

For verification, parse every TOML file, check the custom agent required fields and role/model assignments, and validate supported configuration keys with the installed Codex client or official schema. No application build is needed for template-only changes. An agent execution smoke check belongs in the target trusted project with its configured provider.

For command hook changes, run `python3 -B -m unittest discover -s tests -v` from the starter root. The tests inspect commands without executing them.
