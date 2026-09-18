# 1. Product scope and architecture / 产品与架构

## Define the experience before choosing APIs

Write a concrete user story and a measurable first-release boundary. For a listening companion, “translate continuously” means a session that keeps accepting new speech, translates eligible material, and speaks the result without requiring a tap for each sentence. It does not establish infinite execution under every iOS interruption.

For an English-learning app, the useful loop may instead be: record or import → transcribe → replay a difficult passage → inspect a word → save it → review later. Short-section transcription is not simultaneous interpretation; the listing must say what the app actually does.

Separate three language choices:

- Interface language: labels, settings, permissions, help.
- Source/target language: what speech is recognized or translated.
- Learning content language: definitions, examples and pronunciation.

A user switching the UI to Chinese should not unexpectedly change the recognized language or TTS voice. Use a string catalog or localized resources; check placeholder arguments and translated permission descriptions. Localization is more than a language picker.

## Choose a complete default path

Apple frameworks can supply speech recognition, translation, text-to-speech, and, on eligible devices, model-generated explanations. Availability depends on OS version, hardware, language, region, settings and downloaded assets. Test framework availability at runtime and show a useful fallback or explanation.

A minimum iOS version does not prove every device running that version supports every model. An initial model download means “on device” need not mean “never needs network setup.” Do not claim an Apple model is available before the actual availability API and device behavior establish it.

| Path | Benefits | Product obligations |
|---|---|---|
| Apple on-device features | No provider API token bill for local inference; useful private default | Asset preparation, eligibility checks, cancellation, fallback, real-device validation |
| Optional customer-configured Azure | Alternative transcription/context provider | Explicit transfer consent, user key handling, endpoint compatibility, costs, cloud cancellation, privacy disclosure |
| Bundled authored sample | Reviewable onboarding without account or microphone permission | Clearly label sample content; never silently replace failed live functionality with a demo |

Do not copy a cloud configuration or key from another installed app. A new app must ask the customer to configure its optional provider through the intended secure UI.

## Audio behavior is architecture

**Live listening companion:** keep capture ownership stable during TTS. Decide how finalized speech is queued, bounded, deduplicated and cancelled. A level slider should change assistance density, not merely cosmetic wording. A sparse hint must remain useful after its delay; expire stale hints and preserve explicit “help with everything” requests.

**Recording/replay app:** use a clearly documented policy for recording while playing pronunciation or another passage. One reliable first release stops and saves capture before playback. Save on interruptions/background transitions if background capture is not supported. Do not invent a background capability just to keep a spinner moving.

In both cases:

- Bound buffers and tasks; invalidate async results when the session ends or mode changes.
- Treat headphone removal as a route change with privacy consequences. Do not send private audio to the speaker automatically.
- Speaker mode can feed generated speech back into recognition. Voice processing and realistic acoustic checks are necessary; a callback saying “speaking” is not an echo test.
- Audio-session reconfiguration by a speech helper can stop live capture. Centralize session ownership.
- Retain original audio when the product promises retention. Deleting a transcript or retrying cloud work must not silently destroy the original.

## Durable recordings and timing

Write a recovery marker before a recording section begins. Close and synchronize audio before marking the section finalized. Persist the actual section start time; recovering a file must not shift its transcript to time zero.

Audio converters must honor requested frame counts and drain to end-of-file. Duration changes and silent sections are not harmless formatting problems. A successful upload response does not prove the input contained the full original recording.

Only expose sentence replay when the provider supplies reliable sentence timing. If a provider returns section text without word timestamps, label and replay an “Audio section.” Do not fabricate precise timing from string length.

Use owned or appropriately licensed dictionaries and sample audio. Keep attribution and license text in the app or a reachable credits page. An estimated syllable boundary should be described as an estimate.

**中文要点：** 先确定真实用户流程，再选择 API。本机能力需要检查设备和模型可用性；示例内容必须标记。实时翻译与录音回听是两种不同的音频架构，不应共用未经验证的会话行为。界面语言、翻译方向、学习内容语言必须独立。
