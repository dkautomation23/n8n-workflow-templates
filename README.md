# n8n-workflow-templates

A small, practical set of **ready-to-import [n8n](https://n8n.io) workflows** for
the jobs that come up again and again: capturing leads, digesting feeds, and
pushing form submissions into a CRM without duplicates.

Each file is a clean n8n export — import it, plug in your credentials, and run.

## Templates

| File | What it does |
|---|---|
| [`lead-webhook-to-google-sheets.json`](templates/lead-webhook-to-google-sheets.json) | `POST` webhook → normalise `name / email / source` + timestamp → **append a row to Google Sheets**. A zero-maintenance lead capture endpoint. |
| [`rss-digest-to-slack.json`](templates/rss-digest-to-slack.json) | Every morning at 08:00 → read an RSS feed → keep the last 24h → **post a single digest message to Slack**. Swap the feed URL for any source. |
| [`form-to-crm-dedupe.json`](templates/form-to-crm-dedupe.json) | Contact-form webhook → lowercase/trim → **drop emails already seen in previous runs** → create the contact via HTTP API → respond `{"status":"received"}`. |

## Import

1. In n8n: **Workflows → ⋮ → Import from File** (or paste the JSON via *Import from URL/Clipboard*).
2. Open each node marked with a credential (Google Sheets, Slack) and select your
   own connection.
3. Replace the placeholders:
   - `YOUR_SHEET_ID` — your Google Sheet document id.
   - `#digest` — your Slack channel.
   - `https://api.your-crm.example/...` — your CRM endpoint.
4. Activate the workflow (webhook-based ones give you a production URL once active).

## Notes

- Built and JSON-validated against the n8n export schema (nodes / connections /
  typeVersion). No credentials or secrets are included — every auth field is a
  placeholder you fill in.
- Node type versions target recent n8n (2024–2025). If a node shows as outdated
  on a very old instance, n8n will offer to migrate it on import.

## License

MIT — see [LICENSE](LICENSE).
