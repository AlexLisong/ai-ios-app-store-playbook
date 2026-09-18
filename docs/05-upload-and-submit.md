# 5. Upload, process and submit / 上传与提交审核

## Keep one release identity

Privately record project/scheme, bundle identifier, team, marketing version, build number, source commit and archive path. Confirm all refer to the same release before uploading. If the account can access multiple teams, verify the currently selected team and app before every write.

A team selection in one App Store Connect tab may affect other tabs in the same session. Do not mistake a redirect caused by team context for missing permission. Recheck the intended team and app after another session changes account context.

## Organizer upload

1. Build the final archive after release edits and relevant checks.
2. Open Window → Organizer → Archives and select the correct app/version/build.
3. Choose Distribute App and the App Store Connect upload path.
4. Review signing/account selection and the validation summary. Let Xcode manage supported signing assets.
5. Complete the upload and inspect its actual result. “Uploaded to Apple” is evidence of transfer, not processing or review submission.

The app record may be created in App Store Connect before upload or through a supported Xcode flow. An observed first registration succeeded server-side but the immediate follow-up query reported that no app existed. Rechecking App Store Connect, allowing propagation, and restarting the distribution flow resolved it. Do not create a second identifier or duplicate app record solely because of that immediate stale result.

Wait for processing; inspect any processing email/warning in the proper account. Resolve export-compliance questions if requested. Select the processed build on the release version page and confirm its version, build, icon and supported platform.

If production source changed after upload, determine whether the uploaded binary contains that change. DEBUG-only test-harness fixes can differ without changing a Release binary, but document the evidence; never wave away a functional release change as “only local.”

## App Store Connect completion order

A productive order is:

1. App information: correct app identity, category, content rights and localized name/subtitle.
2. Version metadata: descriptions, keywords, URLs and screenshots for each locale.
3. App Privacy: policy URL, complete answers, then publish the privacy label as required.
4. Age rating: answer the current questionnaire and save its calculated result.
5. Pricing/availability: price, countries, future-country behavior and device distribution choices.
6. Review information: private contact, sign-in requirement, accurate instructions and any necessary dedicated review access.
7. Select the processed build and resolve compliance/export fields.
8. Confirm the release option, save and use the page's final validation.

These sections can move in Apple's UI. Follow the current labels rather than a brittle coordinate script. A successful Save on one section does not mean all sections are complete.

## The final submission is a separate action

Use **Add for Review** when the version is ready. Inspect validation errors and fix the concrete missing requirement. Then open the review submission, confirm the intended version/items, and perform the final **Submit for Review** action when authorized.

In the observed interface, Add for Review produced a Draft Submission dialog. The final Submit for Review action produced “1 Item Submitted”; Go to App Review then showed Waiting for Review. Treat these as observed UI steps, not permanent button names.

Reopen the review status. Record the exact observed state, timestamp and private submission identifier in a private [receipt](../templates/release-receipt.md). The expected next state is often Waiting for Review, but report whichever state Apple actually shows.

A blank main panel immediately after navigation can be a transient load. Wait briefly and inspect fresh state. Do not infer authentication failure or retry writes blindly. Repeated submission clicks can create confusion about what actually happened.

## Verify after submission

Confirm that the submitted version, build, locales, price and countries are the intended ones. Keep the source commit and archived binary associated with that receipt. Mark the review status page as the user's handoff/deliverable in browser tools that support it.

Respond to Apple review issues with the exact failure and a tested correction. A replacement binary requires the appropriate incremented build and another upload. After approval, verify release timing, actual storefront availability in intended territories, install/update behavior and support URLs. Do not claim public availability while the state is only Waiting for Review.

## Suggested final messages

**Uploaded only:** “Version 1.0 (1) uploaded and processed. Submission is still blocked by the missing localized screenshots.”

**Submitted:** “Version 1.0 (1) is submitted and App Store Connect shows Waiting for Review. Apple approval and public availability are pending.”

**Released:** “Apple approved the release, and the app's product page is available in the verified storefronts.” Use this only after both facts were observed.

**中文要点：** 先上传，等待处理，选择 build，补齐资料，再提交审核。最后重新进入状态页，准确说“等待审核”“已通过”或“已上架”，不要把其中一个状态当成另一个。
