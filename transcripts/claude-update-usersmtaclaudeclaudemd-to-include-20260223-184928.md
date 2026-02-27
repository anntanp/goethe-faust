# Transcript: 74a58e20-7771-40b1-8f73-b0461a3668ab

**Project:** /Users/mta/Documents/claude  
**Messages:** 14

---

### User *(2026-02-23T18:49:28.082Z)*

Update /Users/mta/.claude/CLAUDE.md to include this requirement:
- All scripts created should be documented properly.

---

### Assistant *(2026-02-23T18:49:31.731Z)*

**Tool call:** `Read`
```json
{
  "file_path": "/Users/mta/.claude/CLAUDE.md"
}
```

---

### User *(2026-02-23T18:49:33.820Z)*

**Tool result**
```
     1→# CLAUDE.md
     2→
     3→This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
     4→
     5→## Role
     6→
     7→I am a researcher and developer. My work spans two modes:
     8→- **Articles**: technical writing, research summaries, tutorials, documentation, and blog posts
     9→- **Software**: prototypes, tools, scripts, and production solutions
    10→
    11→## Writing
    12→
    13→- Be concise and precise. Prefer plain language over jargon unless the audience is technical.
    14→- Use active voice.
    15→- When drafting or editing articles, preserve my voice — refine, don't rewrite.
    16→- Structure long-form content with clear headings; use bullet points only when items are genuinely list-like, not to fragment prose.
    17→- Cite sources inline when drawing on specific claims; flag anything that needs verification.
    18→
    19→**Experimental articles**
    20→- When an article involves an experiment or empirical claim, proactively suggest an experimental design: what to vary, what to hold constant, and what a suitable control or baseline looks like.
    21→- Recommend evaluation strategies appropriate to the claim — quantitative metrics, qualitative rubrics, ablations, or comparisons — and flag when a chosen metric may not capture what actually matters.
    22→- Include or prompt for error analysis: where does the approach fail, under what conditions, and what do the failure modes reveal about the underlying problem?
    23→- Distinguish between results that are statistically or practically significant and those that are suggestive but inconclusive; flag when sample sizes or conditions limit generalizability.
    24→
    25→## Technical blog posts
    26→
    27→- Lead with the problem or motivation — why does this matter to the reader.
    28→- Prefer concrete examples and working code over abstract explanations.
    29→- Assume a technical audience but don't assume familiarity with the specific tool or concept being introduced.
    30→- End posts with a clear takeaway or next step, not a generic summary.
    31→- When helping draft or outline a post, suggest a title and a one-sentence hook.
    32→
    33→## Code
    34→
    35→- Prefer readability over cleverness. Code may appear in articles, so it must be easy to follow.
    36→- Keep scripts and prototypes self-contained where practical (minimal dependencies).
    37→- Add comments only where the logic is non-obvious — not on every line.
    38→- When producing example code for articles, prioritize clarity and correctness over production hardening.
    39→- When building real tools, flag shortcuts taken in prototypes that would need addressing before production use.
    40→
    41→**Security**
    42→- Never hardcode secrets, credentials, or API keys — use environment variables or a secrets manager.
    43→- Validate and sanitize all external input at system boundaries; never trust user-supplied data.
    44→- Avoid common vulnerabilities by default: SQL injection, XSS, CSRF, command injection, path traversal (OWASP Top 10).
    45→- Use parameterized queries for database access; never interpolate user input into SQL strings.
    46→- Apply least-privilege: request only the permissions a script or service actually needs.
    47→- Flag any use of `eval`, dynamic code execution, or shell passthrough as a review point.
    48→- When handling sensitive data (PII, credentials, tokens), note it explicitly and avoid logging it.
    49→- For prototypes that skip security hardening, call out the specific gaps that would need addressing before production use.
    50→
    51→## Product-ready software
    52→
    53→**Specification**
    54→- Before writing code for a non-trivial feature, produce a short spec: problem statement, inputs/outputs, constraints, and success criteria.
    55→- Flag ambiguities in requirements before implementing, not after.
    56→
    57→**Testing**
    58→- Write tests alongside code, not after. Cover the happy path, edge cases, and failure modes.
    59→- Unit tests for logic; integration tests for system boundaries; end-to-end tests sparingly.
    60→- Tests should be readable as documentation — name them to describe behavior, not implementation.
    61→
    62→**CI/CD**
    63→- Every project should have a pipeline that runs lint, type checks, and tests on each push.
    64→- Fail fast: surface errors early in the pipeline before slower steps.
    65→- Deployments should be automated and repeatable; avoid manual steps that can't be scripted.
    66→
    67→**Deployment**
    68→- Prefer immutable deployments (containers, versioned artifacts) over in-place updates.
    69→- Environment config belongs in environment variables, not in code.
    70→- New deployments should be verifiable — include a health check or smoke test.
    71→
    72→**Maintenance**
    73→- Log enough to diagnose failures, not so much that signal is buried in noise.
    74→- Instrument key operations with metrics or traces from the start; retrofitting is harder.
    75→- Document the operational runbook (how to deploy, roll back, and handle common failures) alongside the code.
    76→
    77→## Research workflow
    78→
    79→- When exploring a new topic, surface what is well-established vs. uncertain or contested.
    80→- Distinguish between "this is how it works" and "this is one approach among several."
    81→- If I ask you to summarize a paper or source, include: core claim, method, key findings, and limitations.
    82→- Proactively note when something I'm building or writing touches an area that moves fast (e.g. ML, security) and may be out of date.
    83→
    84→**Literature review**
    85→- When starting a literature review, first map the landscape: identify the main threads, schools of thought, or competing approaches before diving into individual works.
    86→- Group sources thematically, not just chronologically — highlight where works agree, contradict, or build on each other.
    87→- Flag seminal or highly cited works that should be covered, and note any conspicuous gaps (influential authors, venues, or perspectives not yet represented).
    88→- Distinguish primary sources (original research) from secondary sources (surveys, reviews, commentary); weight them accordingly.
    89→- Note methodological diversity across the literature — different evaluation setups, datasets, or assumptions can make results hard to compare directly.
    90→- When coverage feels thin, suggest search terms, venues, or adjacent fields likely to yield relevant work.
    91→
    92→## Collaboration and pair programming
    93→
    94→- When working through a problem together, think out loud: share reasoning, not just conclusions, so I can catch wrong assumptions early.
    95→- If I push back on an approach, engage with the objection rather than restating the original answer.
    96→- Distinguish between "this is the right way" and "this is one valid way" — flag when a choice is a matter of taste vs. a meaningful trade-off.
    97→- Before making a large change, state what you're about to do and why; don't silently rewrite.
    98→- When I take over a section of code or draft, note what you changed and what you left alone.
    99→- If you spot a problem adjacent to the task at hand (a bug, a design smell, an inconsistency), flag it briefly without derailing into fixing it unless asked.
   100→- Keep suggestions additive when reviewing my work — note what's working before what needs changing.
   101→- When we're stuck, offer to reframe: summarize where we are, what we've tried, and what the open question is.
   102→
   103→## General
   104→
   105→- Don't pad responses. If the answer is short, keep it short.
   106→- When I ask for options, give 2–3 concrete choices with trade-offs, not an exhaustive list.
   107→- If a task is ambiguous, state your interpretation before proceeding rather than asking.
   108→
   109→**Response format**
   110→- Lead with the answer or conclusion; put context and caveats after, not before.
   111→- Use markdown formatting: headers for multi-section responses, code blocks for all code and commands, bold for key terms being introduced.
   112→- Use tables for direct comparisons (options, metrics, trade-offs); avoid them for prose that would read naturally as sentences.
   113→- No preamble ("Great question!"), no closing summary ("In summary…") unless the response is long enough that a recap adds genuine value.
   114→- For multi-step explanations, numbered lists; for non-sequential items, bullets; for prose that flows naturally, neither.
   115→- Inline citations or source references in parentheses; don't collect them in a separate section unless there are more than five.
   116→



```

---

### Assistant *(2026-02-23T18:49:38.674Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/.claude/CLAUDE.md",
  "old_string": "- Keep scripts and prototypes self-contained where practical (minimal dependencies).\n- Add comments only where the logic is non-obvious — not on every line.",
  "new_string": "- Keep scripts and prototypes self-contained where practical (minimal dependencies).\n- Document all scripts: include a header comment describing purpose, usage, inputs/outputs, and any dependencies or assumptions.\n- Add comments only where the logic is non-obvious — not on every line."
}
```

---

### User *(2026-02-23T18:49:47.239Z)*

**Tool result**
```
The file /Users/mta/.claude/CLAUDE.md has been updated successfully.
```

---

### Assistant *(2026-02-23T18:49:50.130Z)*

Added to the **Code** section: scripts should have a header comment covering purpose, usage, inputs/outputs, and dependencies/assumptions. Placed it alongside the existing self-contained scripts guideline where it fits naturally.

---

### User *(2026-02-23T18:51:00.851Z)*

Update /Users/mta/.claude/CLAUDE.md to include this requirement:
- maintain an .md file that documents scripts created.

---

### Assistant *(2026-02-23T18:51:04.753Z)*

**Tool call:** `Edit`
```json
{
  "replace_all": false,
  "file_path": "/Users/mta/.claude/CLAUDE.md",
  "old_string": "- Document all scripts: include a header comment describing purpose, usage, inputs/outputs, and any dependencies or assumptions.",
  "new_string": "- Document all scripts: include a header comment describing purpose, usage, inputs/outputs, and any dependencies or assumptions.\n- Maintain a `SCRIPTS.md` file in the project root listing every script: name, purpose, usage, and any notable caveats. Update it whenever a script is created or significantly changed."
}
```

---

### User *(2026-02-23T18:51:14.269Z)*

**Tool result**
```
The file /Users/mta/.claude/CLAUDE.md has been updated successfully.
```

---

### Assistant *(2026-02-23T18:51:17.120Z)*

Added the `SCRIPTS.md` requirement directly after the per-script header comment rule, so both documentation requirements sit together in the **Code** section.

---

### User *(2026-02-23T18:51:49.948Z)*

Reload /Users/mta/.claude/CLAUDE.md for all active sessions

---
