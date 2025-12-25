# session-management

6-phase workflow coordination for session management. Manages context across sessions, implements checkpoint/resume patterns, and tracks progress through complex multi-step tasks. Use when: starting new sessions, resuming work, managing long-running tasks.

## Metadata
- **Version**: 1.0.0
- **Category**: productivity
- **Source**: workspace


## Tags
`session`, `workflow`, `context`, `coordination`, `checkpoint`

## MCP Dependencies
None specified

## Inputs
- `action` (string) (required): Action: start, resume, checkpoint, summary, handoff
- `sessionId` (string) (optional): Session identifier for tracking
- `context` (string) (optional): Current context or summary to persist

## Chain of Thought
1. Identify current session state (new/existing). 2. For new sessions: scan CLAUDE.md, check git status, identify active tasks. 3. For resume: load last checkpoint, summarize progress, identify next steps. 4. Create checkpoint with: completed items, current state, open items, blockers. 5. For handoff: generate comprehensive summary for next session.


## Workflow
No workflow defined

## Anti-Hallucination Rules
None specified

## Verification Checklist
None specified

## Usage

```typescript
// Execute via MCP Gateway:
gateway_execute_skill({ name: "session-management", inputs: { ... } })

// Or via REST API:
// POST /api/code/skills/session-management/execute
// Body: { "inputs": { ... } }
```



## Code

```typescript
// Session Management Skill
const action = inputs.action || 'start';
const sessionId = inputs.sessionId || new Date().toISOString().split('T')[0];

const phases = {
  start: `SESSION START - ${sessionId}
1. Context Loading: Scan CLAUDE.md and project state
2. Task Discovery: Identify TODOs, open issues, recent commits
3. State Assessment: Check uncommitted changes, branch status
4. Priority Setting: Rank tasks by urgency and dependencies
5. Plan Creation: Outline session objectives
6. Checkpoint Ready: Enable progress tracking`,

  resume: `SESSION RESUME - ${sessionId}
1. Load Previous State: Retrieve last checkpoint
2. Progress Review: What was completed vs planned
3. Context Restoration: Reload relevant files/decisions
4. Blocker Check: Any new issues since last session
5. Priority Refresh: Adjust based on new information
6. Continue Work: Pick up from last checkpoint`,

  checkpoint: `CHECKPOINT - ${sessionId}
- Completed: [List completed items]
- In Progress: [Current task state]
- Blocked: [Any blockers encountered]
- Next Steps: [Planned next actions]
- Context: ${inputs.context || 'No additional context'}`,

  summary: `SESSION SUMMARY - ${sessionId}
Accomplishments: [What was achieved]
Decisions Made: [Key decisions with rationale]
Open Items: [Remaining tasks]
Handoff Notes: [What next session needs to know]`,

  handoff: `SESSION HANDOFF - ${sessionId}
## For Next Session:
1. Current State: [Detailed current state]
2. Last Action: [What was just done]
3. Next Action: [What should happen next]
4. Context Files: [Key files to review]
5. Warnings: [Gotchas or issues to be aware of]`
};

console.log(phases[action] || phases.start);
```

---
Created: Tue Dec 23 2025 00:30:23 GMT+0800 (Singapore Standard Time)
Updated: Tue Dec 23 2025 00:30:23 GMT+0800 (Singapore Standard Time)
