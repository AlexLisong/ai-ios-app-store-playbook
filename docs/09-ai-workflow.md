# 9. Reusable AI workflow / 可复用 AI 工作流

## English starter prompt

Copy this into your coding assistant after replacing bracketed choices. Keep actual account details and credentials out of the prompt; supply them only through appropriate secure interfaces when needed.

```text
Build and prepare a native iPhone app for this user outcome: [outcome].
Use [English and Simplified Chinese] UI. The first release includes [features]
and excludes [out-of-scope features]. Default processing is [on device].
Optional provider mode is [none / customer-configured Azure with their own key].

Read the repository instructions, inspect existing implementation and release
records, and write a concrete acceptance plan. Continue useful authorized work
without repeatedly asking for permission. Ask only for missing decisions that
change product/legal facts or for protected actions I must do myself.

Use a complete default experience with honest runtime availability checks.
Keep interface language separate from recognized/translated/spoken language.
Do not silently replace real functionality with sample content or cloud fallback.
Never reuse another app's keys or upload personal recordings for tests.

Verify logic, native UI, and the intended physical-device workflows. Clearly
separate simulator, authored-audio, microphone/acoustic and live-provider evidence.
Fix demonstrated failures and record meaningful remaining limitations.

Prepare an original icon, native-size English/Chinese screenshots, matching store
metadata, privacy answers, review notes, and public support/privacy pages on the
existing authorized hosting setup. Keep private contacts and operational IDs in
ignored private files, not public source or screenshots.

Release choices: [free/no ads/no purchases], [Canada and United States only],
[automatic release after approval], [iPhone only]. Confirm legal/trader facts
from information I actually provide; never infer them from pricing.

Publication authorization: [prepare only / upload only / submit for App Review].
Within that scope, use Xcode automatic signing with the intended signed-in account.
Do not bypass protected OS/browser controls. I will handle passwords, two-factor
authentication, phone trust/unlock, and protected Keychain dialogs directly.

If authorized to submit, complete the final review submission after upload,
processing, build selection and all required listing fields. Verify actual status.
Save a private release receipt tying source commit to archive, version/build,
validation and App Store state. Do not claim approval or availability prematurely.
```

## 中文启动提示词

```text
请开发并准备发布一款原生 iPhone 应用，解决：[用户问题]。
界面支持英文和简体中文。首版包括：[功能]；暂不包括：[范围之外]。
默认采用：[本机处理]。可选云端功能：[无 / 用户自配 Azure 资源和密钥]。

先阅读仓库说明，检查已有实现与发布记录，建立具体可验证的验收计划。
在已经授权的范围内持续完成工作，不要反复询问同一件事是否允许。
只有缺少会影响产品/法律事实的决定，或者需要我操作受保护的系统界面时，
再提出明确的问题。等待我操作时，继续完成不依赖该操作的准备工作。

界面语言与识别/翻译/播放语言分开。正确处理 Apple 模型的设备兼容性与下载。
演示内容必须明确标记；不要用演示代替失败的实时功能，也不要悄悄改为云端。
不要复用其他应用的密钥，不要用私人录音做测试。

完成适当的逻辑、UI 和真机验证。分别记录模拟器、样例音频、真实麦克风、
声学路线和真实云端请求的证据。修复已经确认的问题，明确剩余限制。

准备原创图标、正确尺寸的中英文真实应用截图、商店文案、隐私回答、审核说明，
以及已有授权域名上的支持/隐私页面。真实联系人、账号标识和运维信息只放私有
文件或平台私有字段，不要放进公开仓库、截图或日志。

发布选择：[免费/无广告/无内购]，[仅加拿大和美国]，[审核通过后自动发布]，
[仅 iPhone]。法律和经营者身份根据我提供的事实填写，不要根据免费推断。

本次授权：[仅准备 / 上传 / 提交 App Review 审核]。
使用正确的 Xcode 已登录账户与自动签名；不要绕过操作系统或浏览器安全限制。
密码、双重验证、手机信任/解锁和受保护钥匙串对话框由我直接操作。

如果已授权提交，上传后继续等待处理、选择 build、补齐资料并完成最终审核提交。
最后重新确认实际状态，保存私有发布回执。不要把上传成功说成已提交，
也不要把等待审核说成已通过或已上架。
```

## Continue from an interrupted release

```text
Continue the existing release. First read its private release receipt and inspect
current Xcode/App Store Connect state. Preserve earlier authorization and decisions.
Do not create duplicate app records or repeat completed uploads. Verify the active
team, app, version/build and browser identity before changes. Complete remaining
authorized work and update the receipt with observed evidence.
```

## Ask for the smallest protected handoff

Good: “The archive is ready. Xcode is showing a protected Keychain prompt for codesign. Please enter your Mac password in that system dialog and allow the request.”

Good: “The screenshot upload is blocked by the extension's local-file permission. Please enable Allow access to file URLs for the connected extension, then I will retry the inspected screenshot files.”

Do not ask the owner to hand over passwords or paste production keys in chat. Do not frame a tool limitation as proof that an alternative supported workflow is impossible. For example, a browser certificate download block does not rule out Xcode-managed distribution.

## Parallel work without shared-state collisions

If the user or repository instructions authorize delegation, useful independent tasks include metadata/privacy drafting, static support pages, and code review. Keep one owner for Xcode/physical-device UI and App Store Connect mutations. Multiple agents switching browser teams or active native windows can interfere with each other.

Share a small release status record: current version/build, completed steps, blockers, evidence and ownership. Before resuming after context loss, inspect that record and actual platform state instead of trusting a remembered claim.
