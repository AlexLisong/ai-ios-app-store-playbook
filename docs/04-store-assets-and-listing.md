# 4. Icon, screenshots and listing / 图标、截图与商店资料

## Prepare the final visual identity before upload

Use an original icon that reads at small sizes, with a consistent native visual language. A simple vector master is useful for iteration; the App Store asset in this workflow was an opaque RGB PNG at **1024 × 1024**. Validate the asset catalog and inspect small previews. Do not pre-round the corners or use an account screenshot as artwork.

Changing the icon after uploading requires a new binary/build if it changes bundled assets. Finish branding, support links, version labels and privacy copy before the final archive.

## Capture the real application

Use an available simulator that naturally produces a required screenshot size. In the observed workflow, a large iPhone simulator produced **1320 × 2868** portrait screenshots accepted in the 6.9-inch media slot. Other accepted sizes and slot requirements exist; consult [Apple's current screenshot specification](sources.md).

```sh
xcrun simctl list devices available
xcrun simctl io SIMULATOR_UDID screenshot artifacts/screenshots/en-US/01-library.png
```

Create output directories first. Select the actual simulator, launch the final app, and navigate to stable, meaningful content before capture. Use authored, licensed sample material; never capture a user's private recording, contacts, account names, API keys or private review details. Avoid a giant “demo” banner in place of the real feature while still clearly labeling authored examples where they appear.

Prepare each locale independently, for example:

| Order | Screen | Message |
|---|---|---|
| 1 | Main learning/listening screen | What the app helps the user do |
| 2 | Transcript and replay | How a difficult passage becomes usable |
| 3 | Word detail/review | Why the user returns tomorrow |

Inspect full-resolution shots and a contact sheet: no cut-off text, wrong language, loading state, developer overlays, keyboard covering controls or unexplained empty screens. A pretty simulator screenshot is evidence of layout, not live speech accuracy.

Do not stretch a smaller screenshot to satisfy a larger slot. If designing a composed marketing screenshot, preserve accurate app content and follow Apple's current screenshot rules; the simplest verified workflow uses native-size captures.

## Uploads and locale inheritance

App Store Connect's media manager can reuse a 6.9-inch screenshot set for supported smaller device classes. Check its actual preview and requirements; do not fill every historical slot mechanically.

A newly added locale may **inherit the primary locale's screenshots**. In the media manager, edit the relevant device-size set to enable locale-specific images before uploading the translated set. Otherwise the page can appear to have screenshots while still showing English content for Chinese.

Multi-file uploads can finish in a different order from filenames. Verify the rendered order after processing. Check the first screenshot in particular. Save, navigate away and return to confirm persistence.

If an extension's local upload is blocked, see [browser upload troubleshooting](07-troubleshooting.md). Do not repeatedly click file inputs or take over a changing native window without rechecking state.

## Complete store metadata as a coherent product

Use the [metadata template](../templates/app-store-metadata.json). English and Simplified Chinese should describe the same release accurately, with natural copy in each language.

Common current limits include a 30-character name, 30-character subtitle, 170-character promotional text, 100-character keywords and 4,000-character description. Validate against App Store Connect's current field counters, especially for Unicode/localized punctuation. Our repository checker provides an early length check, not Apple's definitive validation.

Include requirements and limits that change the purchase/use decision: iOS/device/model eligibility, initial downloads, foreground-only capture, optional third-party processing, and provider charges. Avoid “never-ending,” “perfect accuracy,” “fully offline” or “zero costs” unless the complete behavior supports the claim.

## Availability and account settings

Example first-release choices were Education, free, no ads, no purchases, English plus Simplified Chinese, and Canada/United States only.

For that scope:

- Set free pricing, verify the schedule, and save.
- Select only Canada and the United States; disable automatic inclusion of future countries if that is the owner's preference.
- Check iPhone/iPad support, Apple silicon Mac availability and Apple Vision Pro availability independently. A universal default can exceed the intended scope.
- Choose automatic or manual release after approval as authorized. Automatic release is still conditional on approval and distribution readiness.
- Answer the current age-rating questionnaire based on actual app content and access. Do not copy a previously calculated 4+ rating blindly.
- Disclose third-party content rights accurately, including licensed pronunciation dictionaries and sample material.
- Resolve export-compliance questions using actual encryption use. An app that only uses exempt standard HTTPS may qualify for an exemption, but do not hardcode `ITSAppUsesNonExemptEncryption=false` without evaluating the app and current guidance.
- EU trader status is a factual account/distribution question. Free apps can still be commercial. Ask the owner for facts rather than inferring non-trader from a zero price; selecting Canada/US alone does not make an unrelated account declaration true.

Public support contact and private App Review contact are different. Use a reviewed public channel on the website, and enter the owner's authorized private details only in Apple's private fields. Generic repository templates must not contain the real entries.

**中文要点：** 用真实应用和正确尺寸模拟器截图。新语言可能继承主语言图片，需要单独编辑。上传完成后核对实际图片顺序。免费、无广告、地区限制和是否允许 Mac/Vision Pro 分发，都要分别保存并复核。
