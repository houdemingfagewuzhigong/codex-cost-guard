# codex-cost-guard

[中文文档](README.zh-CN.md)

Stop discovering your Codex, Claude Code, Cursor, or Copilot agent session cost after the damage is done.

`codex-cost-guard` is a zero-dependency CLI that estimates token burn from local agent transcripts, flags runaway sessions, and emits CSV-style text, JSON, and SARIF for CI.

> Unofficial project. This repository is not affiliated with OpenAI, Anthropic, Cursor, GitHub, or Microsoft. Product names are used descriptively for compatibility.

## Demo

![codex-cost-guard demo](demo/demo.svg)

## Quick Start

```bash
python3 codex_cost_guard.py ./transcripts --max-tokens 120000
```

JSON:

```bash
python3 codex_cost_guard.py ./transcripts --json
```

SARIF:

```bash
python3 codex_cost_guard.py ./transcripts --sarif codex-cost-guard.sarif
```

## Why This Is Useful

Coding agents make it easy to run long loops, paste huge context, or let multiple agents work in parallel. This tool gives you a quick local budget check before a transcript becomes an expensive habit.

It estimates:

- transcript characters
- rough token count
- cost using your chosen USD-per-million-token price
- turn count
- runaway risks such as huge context or long sessions

## GitHub Actions

```yaml
name: Agent Cost Guard

on:
  pull_request:

jobs:
  cost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Estimate agent transcript cost
        run: python3 codex_cost_guard.py ./transcripts --sarif codex-cost-guard.sarif || true
```

## Output Formats

- Text table for local review
- JSON for scripts and dashboards
- SARIF for CI warnings

## Roadmap

- Native parsers for more agent transcript formats
- Per-model price presets
- HTML budget report
- GitHub comment bot mode

## License

MIT
