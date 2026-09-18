# Instructions for AI contributors

This repository is an anonymized release playbook. Keep it safe to share even if it is currently private.

- Never add original developer names, contacts, team/provider/app/device identifiers, real bundle IDs, production domains or infrastructure, local user paths, credentials, signing material, recordings, or account screenshots.
- Use Example Developer, developer@example.com, com.example.app, TEAM_ID, DEVICE_UDID, example.com and /path/to/project. Keep actual operational values in a separate ignored private workspace.
- Explain the difference between built, installed, tested, uploaded, processed, submitted, approved and released.
- Verify changeable Apple/Microsoft guidance against primary sources. Date observations and avoid presenting one account's configuration as a universal rule.
- Use supported tools and existing authorization. Never automate password/OTP entry or bypass a browser/OS security control.
- Run `python3 scripts/check_repo.py` and `python3 -m unittest discover -s tests -v` after changing docs or scripts. Inspect all files before committing; automated scanning is only a supplement.
- Do not add deployment automation that writes to production by default. Existing scripts are read-only local checks.
- Do not commit release receipts filled with real private account details. Templates must remain generic.
