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