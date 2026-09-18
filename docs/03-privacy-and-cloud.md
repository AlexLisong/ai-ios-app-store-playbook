# 3. Privacy and optional Azure / 隐私与可选云端功能

## Follow actual data flows

Three different artifacts must agree: the implemented behavior and consent UI, the public privacy policy, and App Store Connect's privacy answers. A privacy manifest also declares applicable collected-data types and required-reason API use. The manifest does not automatically complete the store privacy questionnaire.

For each feature, write what leaves the device, its destination, purpose, retention, user association, and user controls. Include optional features and SDKs. “We have no backend” does not mean a third-party provider never collects data.

| Behavior | Questions to resolve |
|---|---|
| Local audio, transcript and preferences | Does anything leave the device? What about backups, diagnostics or SDKs? |
| Apple model preparation | What assets are downloaded? What availability limits must the user see? |
| Azure transcription | Which audio sections, endpoint, deployment, geography and service terms? |
| Azure contextual explanation | Which word, sentence/context, response and authentication information? |
| Support email | What does the customer voluntarily send and how is it handled? |

Apple's collection definition concerns off-device transmission that allows the developer or a third party to access data longer than necessary to service the request in real time. Read the exact current [privacy guidance](sources.md). Do not guess that every network request is collection, or that every optional request is exempt.

## A customer key does not remove disclosure obligations

The example cloud-capable app starts in on-device mode every launch. Choosing Azure presents a named Microsoft Azure transfer/cost disclosure. Saving configuration alone does not send a test request. Only eligible new recordings/imports and explicitly selected word context are sent; switching modes does not retroactively upload the existing library.

The implementation stores a provider key in endpoint-bound, device-only iOS Keychain, never UserDefaults, source, analytics or logs. The key must still travel over HTTPS to authenticate requests to its configured provider. “Stored securely” is different from “never transmitted.”

Secure configuration should:

- Validate HTTPS and supported provider hosts before attaching credentials.
- Reject cross-host redirects or other redirects that could leak authentication.
- Store credentials for the chosen endpoint; replacing endpoint/key first revokes active cloud mode.
- Cancel queued and in-flight work when the user withdraws future consent, with stale-result guards.
- Use bounded input/response sizes and reasonable timeouts.
- Preserve source audio; create a temporary provider-compatible format only for upload.
- Never fall back to cloud silently when on-device recognition fails.

Cancellation stops future work as far as possible; it cannot retract a request already received by a provider. Local deletion does not necessarily remove provider-retained data.

## Retention, linking and geography

Microsoft documents deployment-specific behavior and possible abuse-monitoring retention or human review for certain prompts/completions. Customer arrangements can differ. “Not used to train base models” does not mean no retention, review or processing. Do not promise a universal retention duration or universal zero retention without evidence for the supported service configuration.

An app accepting arbitrary compatible customer deployments cannot assume every deployment has the same monitoring, regional processing or preview-service guarantees. Distributing only in Canada and the United States does not constrain a global cloud deployment to those countries.

For the observed Azure-capable design, a conservative assessment disclosed **Audio Data** and **Other User Content**, used for **App Functionality**, linked to the user, without tracking. The rationale included provider resource association, potential retention, and speech/context that was not anonymized. This is a documented example, not a preset answer for all Azure apps.

Do not add “User ID” solely because a cloud resource has an identifier. Establish what end-user identifiers are actually sent or retained. Conversely, renaming a WAV file `audio.wav` does not anonymize a recognizable voice. Apple's guidance treats free-form voice/text as content; do not invent collection of every imaginable field that could occur in a sentence.

The optional-disclosure exception is narrow. A core learning feature issuing repeated requests after one consent is not automatically exempt merely because it is opt-in.

## Consent copy example

> **Use Microsoft Azure?** New audio sections and the words and sentence context you choose will be sent to your configured Microsoft Azure resource. Microsoft processes requests under its applicable terms and your resource settings, which can include retention or review. Usage may be charged to your Azure account. Existing local recordings are not uploaded just by changing modes. You can return to on-device mode to stop future cloud work. Requests already received cannot be withdrawn. [Privacy policy]

> **使用 Microsoft Azure？** 新的音频片段以及你选择的单词和句子语境，将发送到你配置的 Microsoft Azure 资源。Microsoft 会按照适用条款和资源设置处理，可能涉及保留或审核。用量可能由你的 Azure 账户付费。仅切换模式不会上传已有本地录音。切回本机模式可停止后续云端请求；已经被接收的请求无法撤回。[隐私政策]

Adapt this to actual behavior. The confirmation must precede the first transfer. A policy link hidden only on the website does not substitute for an accessible in-app policy link.

## Costs and App Review

On-device inference does not incur Azure/LLM API token charges. The app can still require a paid developer membership, hardware and support hosting. Azure is billed according to the customer's actual services; a free app is not a promise of free provider usage.

Give reviewers a complete default path that does not require a production secret. A clearly labeled sample can demonstrate replay, word lookup and vocabulary review; it is not proof of live speech. If Apple needs cloud access, arrange a dedicated limited-quota resource through the private reviewer channel and revoke it appropriately afterward. Never bundle a real key or publish it in review-note source files.

Use [privacy-policy.md](../templates/privacy-policy.md) as a drafting structure. Do not paste an unfinished template onto a public website.
