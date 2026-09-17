# n8n-workflow-templates

[![CI](https://github.com/dkautomation23/n8n-workflow-templates/actions/workflows/ci.yml/badge.svg)](https://github.com/dkautomation23/n8n-workflow-templates/actions/workflows/ci.yml)

A small, practical set of **ready-to-import [n8n](https://n8n.io) workflows** for
the jobs that come up again and again: capturing leads, digesting feeds, pushing
form submissions into a CRM without duplicates, and receiving authenticated
webhooks that answer with a proper status code.

Each file is a clean n8n export — import it, plug in your credentials, and run.

## Templates

| File | What it does |
|---|---|
| [`lead-webhook-to-google-sheets.json`](templates/lead-webhook-to-google-sheets.json) | `POST` webhook → normalise `name / email / source` + timestamp → **append a row to Google Sheets**. A zero-maintenance lead capture endpoint. |
| [`rss-digest-to-slack.json`](templates/rss-digest-to-slack.json) | Every morning at 08:00 → read an RSS feed → keep the last 24h → **post a single digest message to Slack**. Swap the feed URL for any source. |
| [`form-to-crm-dedupe.json`](templates/form-to-crm-dedupe.json) | Contact-form webhook → lowercase/trim → **drop emails already seen in previous runs** → create the contact via HTTP API → respond `{"status":"received"}`. |
| [`authenticated-webhook-with-validation.json`](templates/authenticated-webhook-with-validation.json) | `POST` webhook behind **Header Auth** → check that `order_id / customer_id / total` are present → hand the order to a sub-workflow → answer **200** with the stored record, **400** on missing fields, **403** without the key. |
| [`order-processing-subworkflow-dedupe.json`](templates/order-processing-subworkflow-dedupe.json) | Callable sub-workflow: **look the record up in a data table first**, insert only if it is new, call the processing API, write the result back, and return a consistent payload for both the new and the duplicate path. |
| [`retry-flaky-api.json`](templates/retry-flaky-api.json) | A request against an endpoint that fails intermittently, with **Retry On Fail** configured (5 tries, 1s apart) so transient 5xx clears itself instead of ending the run. The setting lives on the node's Settings tab, not in its parameters — which is why it is easy to think you enabled it when you did not. |
| [`error-workflow-report-failures.json`](templates/error-workflow-report-failures.json) | An **Error Trigger** workflow: catches any linked workflow's failure and posts the workflow name, execution URL, error message and failing node to an endpoint of your choice. Set it under *Settings → Error workflow* on the workflows you want covered. |

## Import

1. In n8n: **Workflows → ⋮ → Import from File** (or paste the JSON via *Import from URL/Clipboard*).
2. Open each node marked with a credential (Google Sheets, Slack) and select your
   own connection.
3. Replace the placeholders:
   - `YOUR_SHEET_ID` — your Google Sheet document id.
   - `#digest` — your Slack channel.
   - `https://api.your-crm.example/...` — your CRM endpoint.
   - `https://api.your-service.example/orders/process` — your order-processing endpoint.
   - `YOUR_X_API_KEY` / `YOUR_X_ASSESSMENT_ID` — header values for your own service.
   - `orders` — the name of your n8n data table (used by the sub-workflow).
4. Activate the workflow (webhook-based ones give you a production URL once active).

## Notes

- Built and JSON-validated against the n8n export schema (nodes / connections /
  typeVersion). No credentials or secrets are included — every auth field is a
  placeholder you fill in.
- Node type versions target recent n8n (2024–2025). If a node shows as outdated
  on a very old instance, n8n will offer to migrate it on import.
- The two order templates are designed to work together: import both, then point
  the `ExecuteProcessOrder` node in the webhook workflow at the sub-workflow.
  The sub-workflow is what makes repeated deliveries safe — webhooks retry, and
  without a lookup before insert you end up with duplicate rows.

- Two gotchas worth knowing before you rely on the error workflow: it only fires on
  **automatic** executions, so pressing *Execute workflow* in the editor will never
  trigger it, and it has to be published itself before it can be selected. Both are
  easy to miss and both look like "the error workflow doesn't work".

## License

MIT — see [LICENSE](LICENSE).
