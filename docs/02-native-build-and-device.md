# 2. Native build, signing and device checks / 编译、签名与真机

## Establish a reproducible project

Use native SwiftUI where it fits the product. Keep deterministic core logic separate from platform audio/UI services so it can be checked without a phone. If a script generates the Xcode project, commit the generator and regenerate after adding source, resources or test targets. A source file on disk is not necessarily in a build phase.

Set a unique bundle identifier, display name, deployment target, supported device family, app icon, version and build number. For release, verify the resolved values inside the **built** app rather than assuming source Info.plist settings won.

`CFBundleShortVersionString` is the marketing version; `CFBundleVersion` identifies the build. Increment the build number for a new upload that changes the binary. Once uploaded, changing local source does not replace that build. Do not publish the same version/build pair again and assume Apple will overwrite it.

## Start with Xcode-managed signing

1. Sign in to the intended Apple Account in Xcode Settings → Accounts. The account owner completes password and verification prompts directly.
2. Select the correct development team under Signing & Capabilities and enable Automatically manage signing.
3. Confirm the account has membership and App Store Connect permissions for the app. Resolve relevant agreements through the account owner when required.
4. Build for a connected device or Generic iOS Device. Use Archive for distribution; an unsigned SDK build is only a compile check.
5. Use Organizer → Distribute App → App Store Connect and the supported automatic signing flow. Exact screens vary by Xcode version.

A browser certificate download blocked by organization policy is not a reason to disable that policy. The observed workflow succeeded with Xcode-managed distribution after account sign-in. Depending on account permissions and configuration, Xcode can manage signing assets, including cloud-managed distribution. This is not a guarantee that every team/account needs no signing setup.

Avoid selecting one of several same-named development certificates by a brittle name match. Prefer the project's automatic signing configuration. Never export a private key or put a distribution profile in the repository just to “make the build work.”

## Safe command examples

Replace placeholders locally. These commands contain no account secrets. Build artifacts may contain identifying information and belong in a private, ignored directory.

```sh
xcodebuild -version
xcodebuild -list -project ExampleApp.xcodeproj
xcrun simctl list devices available
xcrun devicectl list devices
```

For a compile-only check:

```sh
xcodebuild -project ExampleApp.xcodeproj -scheme ExampleApp \
  -configuration Release -destination 'generic/platform=iOS' \
  -derivedDataPath artifacts/DeviceBuild \
  CODE_SIGNING_ALLOWED=NO build
```

For a real device test, select its actual identifier privately:

```sh
xcodebuild -project ExampleApp.xcodeproj -scheme ExampleApp \
  -destination 'platform=iOS,id=DEVICE_UDID' \
  -resultBundlePath artifacts/DeviceTests.xcresult test
```

Archive after final release edits:

```sh
xcodebuild -project ExampleApp.xcodeproj -scheme ExampleApp \
  -configuration Release -destination 'generic/platform=iOS' \
  -archivePath artifacts/ExampleApp-1.0-build1.xcarchive \
  -allowProvisioningUpdates archive
```

`-allowProvisioningUpdates` permits Xcode to manage signing with the configured account; it does not log in or grant permissions. On a workspace-based app, use `-workspace` instead of `-project`. Use the scheme's actual tests and destinations; generic commands do not substitute for project instructions.

## Pairing, lock and protected prompts

Pairing may require the owner to unlock the iPhone, tap Trust, enter the passcode, or enable Developer Mode and restart when iOS asks. A phone can be connected and installed yet still refuse launch because it is locked.

Keep it unlocked during interactive device tests. If a protected macOS Keychain dialog asks to allow codesign to use a key, the owner enters the Mac login password directly and chooses Allow when appropriate. Do not script around protected dialogs or ask the owner to paste a password into chat.

Useful handoff: “Xcode is waiting to launch the test app because the connected iPhone is locked. Please unlock it and keep it unlocked while the tests run.” After the reply, retry the blocked operation and verify its result.

## Inspect the final app bundle

```sh
python3 /path/to/playbook/scripts/preflight.py \
  artifacts/ExampleApp-1.0-build1.xcarchive/Products/Applications/ExampleApp.app
codesign --verify --deep --strict \
  artifacts/ExampleApp-1.0-build1.xcarchive/Products/Applications/ExampleApp.app
```

**Packaging pitfall:** a copied folder literally named `Resources` at the root of an iOS `.app` caused CFBundle to classify the result like a legacy macOS bundle and report a missing bundle identifier even though root Info.plist was correct. Inspect the emitted app and use a specific name such as `LearningResources`. This is an observed packaging failure, not a claim that Xcode resource groups are prohibited.

## Tests with honest boundaries

Run the smallest relevant logic/audio/UI checks first. After they pass, broaden testing only when a changed feature or unresolved risk warrants it. Test harnesses must use isolated temporary libraries, especially on a real phone; do not overwrite the user's existing recordings.

A good release record distinguishes package tests, simulator UI tests, physical-device native tests, actual Apple speech inference on authored audio, real microphone checks, acoustic output, and live cloud validation. An API mock proves request construction and failure handling, not a working customer deployment.

**中文要点：** 自动签名优先；编译成功、安装成功、启动成功和功能成功分别记录。手机锁屏、信任配对和钥匙串密码需要用户操作。检查最终 `.app`，不要只看工程设置。
