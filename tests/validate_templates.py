#!/usr/bin/env python3
"""Check every template before it is published or submitted to n8n.

Two jobs. First, that a template still imports: valid JSON, the keys n8n reads,
unique node ids and names, and connections that point at nodes that exist.
Second, and the reason this runs in CI, that nothing private ever rides along in
an export - a credential id from the machine it was built on, a real webhook URL,
an API key, or a live email address.

    python tests/validate_templates.py

Exits non-zero and prints every problem it found, not just the first.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

STICKY = "n8n-nodes-base.stickyNote"

# Things that must never appear in a public export.
SECRETS = [
    (re.compile(r"\bsk-[A-Za-z0-9]{16,}"), "OpenAI-style API key"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}"), "hardcoded bearer token"),
    (re.compile(r"https://hooks\.slack\.com/services/\S+"), "real Slack webhook URL"),
    (re.compile(r"https://[a-z0-9-]+\.app\.n8n\.cloud/webhook/\S+"), "real n8n Cloud webhook URL"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "IP address"),
]

# Addresses that are reserved for documentation and cannot reach anyone.
SAFE_EMAIL_DOMAINS = ("example.com", "example.org", "example.net", "example.invalid")
EMAIL = re.compile(r"\b[\w.+-]+@([\w-]+\.[\w.-]+)\b")


def problems_in(path: Path) -> list[str]:
    found: list[str] = []
    raw = path.read_text(encoding="utf-8")

    try:
        flow = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    for key in ("name", "nodes", "connections"):
        if key not in flow:
            found.append(f"missing top-level key `{key}`")
    nodes = flow.get("nodes") or []
    if not nodes:
        return found + ["no nodes"]

    names, ids = set(), set()
    for node in nodes:
        for key in ("id", "name", "type", "position", "parameters"):
            if key not in node:
                found.append(f"node {node.get('name', '?')!r} is missing `{key}`")
        name, node_id = node.get("name"), node.get("id")
        if name in names:
            found.append(f"duplicate node name {name!r}")
        if node_id in ids:
            found.append(f"duplicate node id {node_id!r}")
        names.add(name)
        ids.add(node_id)

        # A credential exported with its id points at the author's own n8n
        # instance; importing it silently attaches a credential the user has
        # never seen. Only the type and display name belong in a template.
        for cred_type, cred in (node.get("credentials") or {}).items():
            if isinstance(cred, dict) and "id" in cred:
                found.append(f"node {name!r} still carries a credential id for {cred_type}")

    for source, outputs in (flow.get("connections") or {}).items():
        if source not in names:
            found.append(f"connection from unknown node {source!r}")
        for branch in (outputs or {}).values():
            for group in branch or []:
                for link in group or []:
                    target = link.get("node")
                    if target not in names:
                        found.append(f"connection to unknown node {target!r}")

    # Documentation: n8n's template library rejects undocumented workflows.
    if not any(node.get("type") == STICKY for node in nodes):
        found.append("no sticky note - the template library requires a description")
    if all(node.get("type") == STICKY for node in nodes):
        found.append("nothing but sticky notes")

    for pattern, label in SECRETS:
        match = pattern.search(raw)
        if match:
            found.append(f"{label} in the export: {match.group(0)[:24]}...")
    for match in EMAIL.finditer(raw):
        domain = match.group(1).lower()
        # `notexample.com` must not pass as `example.com`, so match the domain
        # itself or a subdomain of it, never a suffix.
        if not any(domain == safe or domain.endswith("." + safe) for safe in SAFE_EMAIL_DOMAINS):
            found.append(f"real-looking email address: {match.group(0)}")

    return found


def main() -> int:
    files = sorted(TEMPLATES.glob("*.json"))
    if not files:
        print(f"no templates found in {TEMPLATES}")
        return 1

    failed = 0
    for path in files:
        found = problems_in(path)
        if found:
            failed += 1
            print(f"FAIL {path.name}")
            for problem in found:
                print(f"       {problem}")
        else:
            print(f"ok   {path.name}")

    print(f"\n{len(files) - failed}/{len(files)} templates valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
