---
name: inventor-runtime-migration
description: Plan or verify moving an Autodesk Inventor 2024 and Vault add-in from .NET Framework 4.8 to an exact Inventor 2026 or later host build.
---

Build a compatibility matrix from the installed Inventor and Vault client update numbers, Autodesk SDK/interop versions, target framework, architecture and deployment tooling. Confirm which build combinations the business needs.

- Keep the 2024 package on .NET Framework 4.8 while support for that host is required. Inventor 2025 began with .NET 8. For updated Inventor 2026.4 and Vault 2026.4, plan for the .NET 10 Windows target and matching SDKs. Check Autodesk's current release notes against the images you will actually deploy.
- Inventory legacy project items, COM and Vault references, platform target, WPF/XAML, WebView2 runtime, package/native dependencies, add-in manifests, installer layout and load paths. Confirm the in-process host can load the resulting artifact.
- If shipping both host generations, keep compatible contracts and domain code shared where practical and isolate version-specific adapters and manifests. Verify old and new pipe clients against supported servers. Keep unrelated UI or toolkit changes out of the migration unless they solve a demonstrated dependency gap.
- Run each Windows build and meaningful unit suite. Smoke-test add-in discovery, activation, UI, a representative Vault operation if applicable, snapshot capture, pipe reconnection and teardown on each supported host. Verify the older package still installs when dual support is required.

[Autodesk Inventor .NET transition](https://help.autodesk.com/view/INVNTOR/2026/ENU/?caas=caas%2Fsfdcarticles%2Fsfdcarticles%2FInventor--Requirements-for-products-affected-by-the-Microsoft--NET-10-transition.html) · [Vault 2026.4 runtime](https://help.autodesk.com/cloudhelp/2026/ENU/Vault-New/files/WN-general-2026_4.htm) · [Autodesk porting guide](https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-API/files/PortToNetCore_Overview.htm)
