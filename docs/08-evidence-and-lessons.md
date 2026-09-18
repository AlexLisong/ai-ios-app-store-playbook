# 8. Evidence, limitations and reusable lessons / 验证边界与经验

These are anonymized observations collected in September 2026. They preserve the engineering lesson without exposing original account or infrastructure details. No status in this file represents a currently identifiable live app.

## Evidence ladder

| Observation | What it establishes | What it does not establish |
|---|---|---|
| Core unit tests pass | Tested logic with defined inputs | Native permissions, model availability or acoustic behavior |
| Unsigned iPhone SDK build passes | Source compiles for the device SDK | Valid signing, installability or App Store acceptance |
| Simulator UI passes | Tested UI/state behavior in simulator | Microphone quality, route behavior, battery/endurance |
| Signed phone install and launch pass | Device deployment and launch | Every feature works under real use |
| Real Apple speech transcribes authored audio on phone | That engine/device/model path worked on those samples | Real microphone capture, fresh-install asset download, every device/language |
| Stubbed Azure transport passes | Request format, cancellation and failure logic | Real endpoint/model/key compatibility or provider billing |
| Human confirms live translation | Basic functional observation in that session | Measured latency, accuracy, echo control or hours of reliability |
| Exact public files match over HTTPS | Correct static content reached the tested URLs | Every browser/layout or future uptime |
| Organizer says Uploaded | Archive transfer completed | Build processed, attached or submitted |
| App Store Connect says Waiting for Review | Review submission accepted into that state | Approval or public distribution |

Store evidence in ignored private artifacts. A release receipt should summarize what was tested and link to private evidence. Do not publish raw `.xcresult`, account screenshots, device inventories or provisioning output in a tutorial.

## Case A: live listening assistance

The product used a graded level of assistance to reduce competing speech: sparse difficult-word hints at one end and fuller translation at the other. The important implementation questions were queue expiry, cancellation, finalized recognition, source preservation and explicit audio routes.

The user requested both Headphones and Speaker modes. The resulting lesson was to treat route policy as part of privacy and usability: removing headphones must not expose private hints on the speaker. Speaker TTS required audio-session ownership and voice-processing work, with realistic acoustic follow-up beyond simulator callbacks.

The release process included a new icon after an earlier upload. That required a later build, and the selected App Store build had to match the final assets. The app followed a local-processing privacy assessment, which could not be copied to the next cloud-capable app.

## Case B: recording-based learning with optional Azure

The product retained original recordings and transcripts, replayed timed material, offered word explanations/pronunciation, and saved vocabulary for review. Default on-device behavior and optional user-configured Azure were distinct modes.

Several useful lessons emerged:

- Durable section metadata and converter EOF/frame handling mattered as much as the transcript UI.
- Cloud eligibility should be established when content is created/imported; changing a mode must not upload the historical library.
- Replacing a key at the same endpoint is still a configuration change that should revoke active cloud work.
- A generic root `Resources/` folder caused a deceptive bundle-ID failure; inspecting built layout solved what appeared to be a signing issue.
- Physical-device tests need their own isolated storage and realistic software-keyboard handling.
- A real Apple speech test on bundled lessons provided stronger evidence than a stub, while still leaving microphone acoustics and live Azure unverified.
- Local screenshot file permission was the final submission blocker after the build/listing were otherwise ready. Preserving browser identity through extension reload resolved the upload path.

## What to measure before making stronger claims

For a live audio app, test long sessions with interruptions, lock/unlock, quiet periods, routes, temperature and battery. Measure time from a useful source phrase to audible assistance. Distinguish recognition errors, translation errors and scheduling delays. Compare assistance levels with real comprehension tasks rather than assuming fewer spoken words always help.

For a recording app, check interrupted saves, recovery, large imports, unusual codecs, external file providers, replay bounds, model availability, device storage and deletion. Verify the promised retention policy and backup explanation.

For Azure, use a dedicated authorized test resource with a budget and nonpersonal audio. Record actual endpoint/deployment/API-version compatibility privately. No customer's production key belongs in a reusable test. Customer-configurable endpoints require a supported configuration contract rather than a claim that “Azure” always works.

## Maintain the playbook

When a release teaches something new, add: observed symptom → cause supported by evidence → smallest correction → verification → remaining limits. Remove stale advice instead of accumulating contradictory steps. Keep [official references](sources.md) current and never turn a one-off workaround into a universal prerequisite.

**中文要点：** 每条成功结论都要对应证据。模拟器截图不能证明真机录音，Mock 不能证明 Azure 可用，上传不能证明已经提交。经验要记录“现象、原因、修复、验证、仍有哪些限制”。
