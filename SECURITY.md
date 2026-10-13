# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | security fixes only |
| < 0.5   | no        |

## Scope

`rpg-dialogue-quest-editor` is an offline desktop authoring tool. It does not
make network requests during normal operation. The attack surface we care
about:

- **Malicious project files** (`.rpgq.json` / `.rpgq.bin`) that try to trigger
  path traversal on import or export.
- **Script embed injection** — dialogue nodes can carry inline script snippets
  for some engine targets. These are *never* executed by the editor; they are
  treated as opaque strings. Report any code path that evaluates them.
- **Adapter deserialization** — third-party adapters may parse untrusted
  binary. Report unsafe `pickle` / `eval` usage.

## Reporting

Email **security@rpg-dq-editor.dev** or open a private advisory on GitHub.
Do not file a public issue for exploitable bugs. We aim to acknowledge within
72 hours and ship a patch within 14 days for confirmed issues.

## Out of scope

- Bugs that require the user to already run untrusted Python.
- Anti-cheat / anti-tamper of the *target games*. This tool authors content;
  it does not inject into running processes.