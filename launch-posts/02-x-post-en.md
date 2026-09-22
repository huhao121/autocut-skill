# X (Twitter) English Launch Post (Global Developers & Creators)

> **Rules (Strict 2026 X Heuristics)**:
> - 0 hashtags
> - No external links in Tweet 1 (link lives in Reply 1)
> - Formula: `X10 - How-I Teardown` (Targeting Bookmarks & Reposts)
> - Char count: ~230 chars (Fits easily under standard 280-char limit)

---

### Tweet 1 (Main Post):

```text
I edit my AI tutorial videos without touching Premiere or CapCut.

The pipeline runs on a brilliant concept from AutoCut: Whisper transcribes raw footage into a Markdown checklist. You uncheck a sentence, and the video cuts out the dead air.

However, the legacy tool relied on MoviePy: after 50 cuts, audio/video clocks drifted by >1s, creating jarring lip desync.

We rebuilt the engine from scratch:
1. Native FFmpeg complex FilterGraph: PTS clocks locked at decoder level (0.00ms drift across 100+ cuts)
2. 0.18s pre-roll + 0.15s post-roll breathing buffers: never clips initial consonants
3. Packaged as a standard AI Agent Skill (Claude Code / Codex compatible)

Just open-sourced it on GitHub.
```

---

### Tweet 2 (Author Reply 1):

```text
GitHub repository: https://github.com/huhao121/autocut-skill

Huge respect to Mu Li for the original Markdown-editing concept.
Pure Python + FFmpeg, zero bloat. Stars and PRs welcome!
```
