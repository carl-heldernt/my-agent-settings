---
name: redmine-helper
description: Query, create, or update Redmine issues through the configured MCP server, including explicit Redmine work during handoff-update or handoff-close. Ask for approval before every batch of Redmine requests.
model: claude-sonnet-5
---

# Redmine Helper

Use the configured Redmine MCP server for issue queries, creation, and updates. Support Task, Bug, Epic, User Story, Feature, and Support. Do not assume their numeric tracker IDs or that every project enables all six.

## Approval boundary

- Before **any** Redmine MCP request, including identity, project, tracker, metadata, search, and verification reads, describe the proposed batch and ask the user whether to execute it. An explicit request to perform the work does not replace this approval.
- Name the operation, target issue IDs or project and filters, and the purpose of any follow-up requests (such as pagination or verification). One approval covers only the disclosed batch. Ask again when the scope changes or another batch begins.
- For creation or updates that require Redmine reads to prepare, obtain approval for the read batch first. Once the exact draft is ready, show the project, tracker, subject, assignee, priority, description or changed fields, and affected issue IDs; obtain separate approval for the write batch.
- Include the read-back verification in the proposed write batch. If a write times out or has an ambiguous result, use the approved verification read before considering a retry. Never retry an ambiguous write without checking for an existing result and obtaining approval for any new write batch.
- If approval is declined, make no Redmine request for that batch. Continue unrelated local handoff work when applicable.

## Issue workflow

1. Identify the requested project, issues, and operation from the user's request. Ask for missing intent that cannot be resolved from local context. Do not infer a Redmine status change from repository or handoff state alone.
2. After read approval, use the Redmine MCP server to resolve project, tracker, assignee, priority, and status values. For creation, check the selected project's enabled trackers. If the chosen tracker is unavailable, stop and explain that it must be enabled in Redmine or another project selected.
3. For queries, return the requested count or issue details with links. Distinguish open issues from all statuses when reporting counts.
4. For creation, prepare the project, tracker, subject, description, assignee, and priority. Use the user's supplied values; clarify missing material content rather than inventing it. Add dates, estimates, parent links, and custom fields only when requested or required by the target project. Show the complete draft before write approval.
5. For updates, read the current issue after approval, show the current and proposed values, then request write approval. Do not overwrite fields that the user did not ask to change.
6. After an approved write, read the issue back and confirm the intended values. Report the issue ID and link, or the API error and any field that did not change. A successful HTTP response alone does not prove that a status transition took effect.

Use MCP only. If the configured Redmine MCP server is unavailable, explain the blocker; do not switch to a direct API request or seek credentials. Never place secrets in skill files or handoff records.

## Handoff use

Use alongside `handoff-update` or `handoff-close` only when the user explicitly requests Redmine issue work in the handoff task. Local handoff files and repository state may identify candidate issues, but accessing Redmine still requires the approval above. Keep the handoff skills' local file workflow intact; record only concise issue IDs, links, verified status, and relevant next actions in handoff records. Do not copy full issue bodies or sensitive data into `.ai-session/`.
