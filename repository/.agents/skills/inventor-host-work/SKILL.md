---
name: inventor-host-work
description: Trace or implement Autodesk Inventor add-in functionality that crosses COM host threading, Windows named pipes, in-memory model snapshots, or WPF/WebView2 UI.
---

Record the actual Inventor build, installed interop assembly, framework target, and a small fixture. Trace add-in activation and teardown, the host-thread dispatch point, and the callers of the code being changed.

- Capture Inventor objects on the established host thread, then map them to detached managed data. Define snapshot identity, units, revision, invalidation on document or model-state changes, and behavior when the source closes. Publish a complete snapshot at once. Keep COM references out of worker queues and pipe/UI payloads.
- Check the pipe protocol's framing and version negotiation, request bounds, same-machine/session access, timeout, disconnect, and shutdown behavior. Check that concurrent readers get a coherent revision. Use Windows pipe access controls supported by the target framework.
- For WPF, trace Dispatcher ownership and window/event lifetime. For WebView2, match trusted origins and validate the bridge message shape. Verify runtime provisioning on the actual add-in host before introducing a dependency.

Use managed fixtures for DTO and client compatibility, then test pipe behavior on Windows. Verify add-in load, one real document operation, and clean shutdown in Inventor. If testing snapshots, include a document/model change and confirm the next reader sees the expected revision.

[Autodesk add-in guide](https://help.autodesk.com/cloudhelp/2026/ENU/Inventor-API/files/CreatingAnAddIn_Overview.htm) · [Windows pipe security](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights) · [WebView2 security](https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/security)
