# Security Policy

## Supported Versions

This repository has no tagged releases yet. Only the latest commit on `main`
is supported. If you're working from an older commit, update to the latest
`main` before filing a report.

## Reporting a Vulnerability

Report privately through GitHub's Private Vulnerability Reporting: open the
repository's [Security tab](https://github.com/dkautomation23/n8n-workflow-templates/security)
and select "Report a vulnerability". If that option isn't available to you,
email hello@dkautomation.dev instead.

Do not open a public issue for a suspected vulnerability.

Expect a first response within 3 business days.

A good report includes:

- Which template is affected (the file path under `templates/`).
- What it exposes or how it misbehaves — a credential, a live endpoint, data
  that leaks on import or on execution.
- The impact: what someone could do with what it exposes.

## Scope

### Treated as a vulnerability here

- A template under `templates/*.json` that embeds a real, live credential,
  API key, or webhook URL instead of a placeholder — for example an
  OpenAI-style `sk-` key, a Slack `xox` token, a GitHub `ghp_` token, an AWS
  `AKIA` access key id, a hardcoded `Bearer` token, or a real
  `hooks.slack.com` or `*.app.n8n.cloud/webhook/` URL.
- A template that carries an exported credential `id` on a node. That points
  an importer's n8n instance at the template author's own stored credential;
  only the credential type and display name belong in a template.
- A template wired to move a credential value in plaintext through the
  workflow itself — printed into a URL, a body field, a sticky note, and so
  on — instead of going through n8n's built-in credential store the way the
  rest of the templates do.
- A gap in `tests/validate_templates.py`'s secret-scan (the `SECRETS`
  patterns, or the `EMAIL` / `SAFE_EMAIL_DOMAINS` check) that would let a
  real secret or a real-looking email pass validation undetected.

### Not treated as a vulnerability here

- A template that requires you to fill in your own n8n credentials through
  n8n's normal credential UI after importing it. That's expected usage, not
  a leak — every template here works that way.
- Placeholder values that are obviously not real, such as `YOUR_SHEET_ID`,
  `#digest`, or `https://api.your-service.example/...` — these are
  documented in the README as fields you replace before activating a
  workflow.
