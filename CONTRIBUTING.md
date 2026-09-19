# Contributing

This is a repository of n8n workflow templates (JSON exports), not a Python
package. There's nothing to `pip install` to use the templates themselves —
download or import a file from `templates/` directly into n8n.

## Environment

Changing or validating a template needs Python 3.12+ and nothing else: the
validator (`tests/validate_templates.py`) only imports `json`, `re`, `sys`,
and `pathlib` from the standard library. There's no `requirements.txt`
because there's no third-party package to install.

This project's convention, even though there's nothing to install today:
each repository gets its own virtual environment, never shared with another
project. That mostly matters once (if) this repo's tooling grows real
dependencies:

```
python -m venv .venv
```

## Validating a template

Before adding or changing a template, run:

```
python tests/validate_templates.py
```

It must pass clean — exit code 0, every file printed as `ok` — before a
template is added or merged. Concretely, it checks each file under
`templates/*.json` for:

- **Valid JSON.** The file has to parse.
- **Structural soundness.** The top-level `name`, `nodes`, and `connections`
  keys are present; every node has `id`, `name`, `type`, `position`, and
  `parameters`; node ids and names are unique; every connection points at a
  node that actually exists.
- **A sticky note.** At least one `n8n-nodes-base.stickyNote` node carrying
  the template's description — and not *only* sticky notes, there has to be
  a real workflow too. This is what n8n's template library requires before
  it accepts a submission, so a template missing one will fail validation.
- **No real secrets.** No OpenAI-style `sk-` key, Slack `xox` token, GitHub
  `ghp_` token, AWS `AKIA` access key id, hardcoded `Bearer` token, real
  `hooks.slack.com` or `*.app.n8n.cloud/webhook/` URL, or bare IP address
  anywhere in the file. No node may carry an exported credential `id` —
  only the credential type and display name belong in a template.
- **No real email address.** Any address found has to sit on `example.com`,
  `example.org`, `example.net`, or `example.invalid`; anything else fails.

## Adding a new secret-scan pattern

If you're adding a pattern to the `SECRETS` list (or tightening the email
check) in `tests/validate_templates.py`: start with a failing test. Add or
edit a template fixture (or an inline test case) that contains the thing the
new pattern should catch, confirm `python tests/validate_templates.py`
actually fails on it, then add the pattern and confirm it passes. A pattern
that nothing ever exercised is unverified.

## Commit style

Short, descriptive sentences, first word capitalized, no trailing period.
Occasionally a `Type: description` form. From this repository's own
history:

```
Validator: match safe email domains exactly, not by suffix
Run the tests in CI on every push
Add retry and error-workflow reliability templates
```

## Pull requests

- `python tests/validate_templates.py` must pass clean before a template is
  added or changed — that's the merge bar, not a suggestion.
- Keep changes scoped to one template or one concern per PR.
- CI must pass.
