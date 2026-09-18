# 7. Troubleshooting / 故障排查

Prefer one observed failure, one targeted correction, and a fresh verification. Do not repeatedly rerun a long release pipeline when only a single field or device state is wrong.

| Symptom | Likely check | Safe next action | Evidence of resolution |
|---|---|---|---|
| iPhone connected but Xcode waits for pairing | Phone trust/passcode/Developer Mode | Owner completes requested phone action | Device is available and the intended operation proceeds |
| Installed but cannot launch | Phone locked | Owner unlocks and keeps device available | Launch succeeds; correct version is running |
| codesign asks for Keychain access | Protected system authorization | Owner enters Mac password in the system prompt | Build continues and signing verifies |
| Browser blocks certificate download | Managed-browser policy | Use the legitimate Xcode account/automatic-signing route | Organizer distribution succeeds; no policy bypass |
| Duplicate certificate names | Brittle identity selection | Restore intended automatic signing/team configuration | Correct signed archive validates |
| No app found immediately after registration | Server propagation or team context | Check App Store Connect, wait/reinspect, restart distribution | Existing correct app is found, no duplicate created |
| Simulator SDK/runtime mismatch | Installed runtime differs from build SDK | Install a supported matching runtime through Xcode tools | Desired destination is available and tests run |
| “Missing bundle ID” despite correct plist | Final bundle layout and root Resources folder | Inspect `.app`; rename copied resource directory if implicated | Bundle inspection/install succeeds |
| New Swift/resource file absent at runtime | Generated project omitted it | Regenerate project and inspect build phases | File is in the emitted bundle or compiled target |
| Screenshot upload “Not allowed” | Extension local-file permission | Enable the correct extension's file URL permission when owner approves | Same-account file upload completes |
| New locale still shows English images | Media inheritance | Edit locale's device-size set and upload translated shots | Saved localized previews are correct |
| Images uploaded in wrong order | Asynchronous multi-file completion | Inspect and reorder actual displayed thumbnails | First/remaining images match intended story |
| Blank main panel after navigation | Transient UI loading | Wait briefly and take a fresh snapshot | Page state stabilizes before another write |
| Unexpected app/team redirect | Shared account team selection | Verify intended team and app in the same session | Correct app identity is visible before editing |
| TTS says it started but no useful audio | Route, silent mode, volume, audio session | Check real device acoustics and selected output | Audible output on the intended route |
| Speaker translation repeats itself | TTS fed into microphone | Check voice processing, queue/capture ownership and real acoustics | Speech remains useful during a realistic conversation |
| Replay duration or audio is truncated | Converter frame counts/EOF | Test full conversion and drain behavior using authored audio | Duration/content preserved; originals untouched |
| Precise replay jumps to wrong words | Provider did not supply timestamps | Use accurate section-level labels and replay | UI no longer claims invented sentence timing |
| Tests alter an existing library | Test root not isolated | Stop; restore safe fixture routing and unique test storage | Tests use synthetic isolated data only |
| Upload succeeded but Add for Review fails | Missing listing requirement | Read validation and finish that specific field | Add for Review succeeds and final submission is made |

## Browser file upload, without fighting the user's windows

Prefer a purpose-built authenticated connector/API or supported browser file chooser where available. For an interactive browser workflow, keep the selected profile/tab identity and use fresh page state.

An extension-backed browser can require **Allow access to file URLs** in its extension Details before its file chooser accepts local screenshots. The owner can enable this in `chrome://extensions` for the correct extension. This is distinct from bypassing a managed certificate-download restriction.

Changing that permission may reload the extension and change the runtime browser ID. Inventory the available surfaces again. Verify the same extension instance, browser profile, tab identity and URL, then rebind that **same browser session**. Do not silently switch to a different account/profile because its ID is easier to access. Reload the relevant page if needed and verify the app/team before writing.

Read the active tool's file-upload documentation. Use its supported `fileChooser.setFiles`-style operation if available; API names and permissions vary. Upload only inspected files. Check thumbnails and saved state afterward.

A native picker is a legitimate fallback when permitted, but shared active windows can move under automation. Pause and reacquire fresh UI state rather than clicking stale coordinates. If cooperation is necessary, ask for a precise brief action/window handoff. Never capture or manipulate a protected password dialog.

## Do not confuse failure classes

- A permission problem is not fixed by regenerating screenshots.
- A locked phone is not fixed by rebuilding the app.
- A failed live cloud request is not explained away by a passing mock.
- A slow page is not automatically an expired login.
- An empty upload slot is not proof the file chooser failed; inspect processing and saved media.
- An old public page after reload is not proof the new release is corrupt; verify bounded hash convergence.

**中文要点：** 先识别是哪一层失败，再修那一层。浏览器扩展重新加载后可能换运行时 ID，但应重新绑定同一个用户会话，不应切换账户。不要重复点击提交，不要用过期坐标操作文件选择器。
