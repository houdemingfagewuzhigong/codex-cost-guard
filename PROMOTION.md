# Launch Promotion

Repository: https://github.com/houdemingfagewuzhigong/codex-cost-guard

## Hot Topic Scout

1. AI coding-agent cost anxiety: developers are running longer Codex/Claude/Cursor sessions and need budget visibility. Heat 9, shareability 8, MVP 9, usefulness 8.
2. Cursor vs Claude Code vs Codex workflows: high comparison traffic, but harder to make a neutral tool. Heat 9, shareability 8, MVP 6, usefulness 7.
3. MCP server safety: still useful, but we already shipped adjacent tools. Heat 8, shareability 7, MVP 7, usefulness 8.
4. Vibe-coded app leak scanner: strong hook, bigger implementation surface. Heat 8, shareability 8, MVP 6, usefulness 8.
5. Agent context pruning: useful but yesterday's project already covered it. Heat 7, shareability 6, MVP 8, usefulness 8.

Winner: agent cost and runaway-session guard. It has a clear anxiety hook and safely uses Codex/Claude/Cursor names as compatibility keywords.

## Hacker News

Title:

Show HN: codex-cost-guard - estimate token burn from Codex/Claude/Cursor logs

Body:

I built a small zero-dependency CLI for a very practical AI coding-agent problem: long agent sessions are easy to start and hard to budget.

`codex-cost-guard` scans local transcript/log files, estimates tokens and rough cost, flags runaway sessions, and emits text, JSON, and SARIF for CI warnings. It is meant for Codex, Claude Code, Cursor, Copilot-style workflows, but it just reads local text/json/jsonl logs.

Repo: https://github.com/houdemingfagewuzhigong/codex-cost-guard

## Reddit r/opensource

I built `codex-cost-guard`, a zero-dependency CLI that estimates token burn from AI coding-agent transcripts.

It scans local Codex/Claude Code/Cursor/Copilot-style logs, estimates tokens and rough cost, flags runaway sessions, and emits JSON/SARIF for automation.

Repo: https://github.com/houdemingfagewuzhigong/codex-cost-guard

What transcript formats should it support next?

## Reddit r/selfhosted

If you run local coding agents or self-host agent workflows, I made `codex-cost-guard`: a tiny Python CLI that estimates token/cost burn from local transcripts and flags runaway sessions.

No service, no telemetry, just local files. Outputs text, JSON, and SARIF.

Repo: https://github.com/houdemingfagewuzhigong/codex-cost-guard

## Reddit r/programming

AI coding agents make it easy to run long loops without noticing cost/context growth. I built `codex-cost-guard` to scan transcript/log files, estimate token burn, flag runaway sessions, and emit JSON/SARIF for CI.

Repo: https://github.com/houdemingfagewuzhigong/codex-cost-guard

## X Short Post

Built codex-cost-guard: estimate token burn from Codex/Claude Code/Cursor/Copilot-style agent logs before the bill surprises you.

Text, JSON, SARIF. Zero deps.

https://github.com/houdemingfagewuzhigong/codex-cost-guard

## X Long Post

AI coding agents make it easy to let a session run long, paste huge context, or run several agents in parallel.

I built `codex-cost-guard` to give those sessions a budget check.

It scans local transcript/log files, estimates token burn and rough cost, flags runaway sessions, and exports text, JSON, and SARIF for CI warnings.

Unofficial, compatible with Codex/Claude Code/Cursor/Copilot-style workflows.

Repo: https://github.com/houdemingfagewuzhigong/codex-cost-guard

## Naming Note

This is an unofficial compatibility/budgeting tool. Product names are used descriptively, not to imply affiliation or endorsement.
