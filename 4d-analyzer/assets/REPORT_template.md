# Report template

Deliver in chat by default. Keep it scannable — the whole thing should read in about a minute.

```markdown
## 4D analysis

**Input:** [single prompt / prompt + output / full conversation / system prompt / SKILL.md]
**Mode:** [Automation / Augmentation / Agency] — [one line on why]

| D | Verdict | Key point |
|---|---|---|
| Delegation | Adequate | Task suits AI, but bundles research and drafting |
| Description | Weak | No audience or format; success criteria unstated |
| Discernment | Not assessable | Single prompt — share the output to assess this |
| Diligence | Not assessable | No sensitive data or usage signals present |

### Delegation — [verdict]
[Anchored feedback. Quote the relevant text briefly. Name the sub-competency:
Problem Awareness / Platform Awareness / Task Delegation.]

### Description — [verdict]
[Product / Process / Performance Description findings, each anchored.]

### Discernment — [verdict]
[If not assessable: one line on what input would make it assessable.]

### Diligence — [verdict]
[Same.]

### What's already working
[Genuine strengths. Omit only if there truly are none.]

---

## Rewrite

[The improved prompt, in a code block so it copies cleanly.]

### What changed and why
- [Change] — *Product Description*: [reason]
- [Change] — *Task Delegation*: [reason]
```

## Notes

- **The verdict table comes first** so the reader gets the shape before the detail.
- **"Not assessable" rows stay in the table.** Dropping them hides the limits of the analysis,
  and the one-line pointer to better input is often the most useful thing in the report.
- **For a conversation**, add a line under the rewrite listing which follow-ups it absorbs.
- **For a SKILL.md or system prompt**, the rewrite is a separate artifact, not an inline
  code block, and the original file is never overwritten.
- **If Delegation recommends splitting**, the Rewrite section becomes the split — two or
  three smaller prompts, each labelled with its job.
