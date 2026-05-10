# Router Implementation Notes

## Design Goal

Router is not an AI agent. It is a deterministic gate.

It only decides:

- which route is matched
- whether goals are mixed
- whether risky project claims lack evidence
- whether coding-agent requests should be blocked in MVP
- which prompt should be loaded next

## Required Combination Rule

```python
if has_risky_claim and not has_evidence_word:
    return blocked("missing_evidence")
```

## MVP Coding Rule

`coding_agent_enabled_in_mvp: false`

When a user asks for code scanning, repository scanning, or commit extraction, the router must block and ask the user to manually provide evidence.

## Why not LLM routing?

LLM routing is flexible but uncertain. This skill needs predictable blockers first.

Use keyword routing for MVP. Add manual confirmation for ambiguous cases.
