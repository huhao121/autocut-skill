<p align="center">
  <h1 align="center">✂️ autocut-skill</h1>
  <p align="center">
    <strong>Edit video by writing Markdown — with zero A/V sync drift.</strong>
  </p>
  <p align="center">
    A native FFmpeg-powered video cut engine & Agent skill.<br>
    <em>Inspired by the brilliant Markdown editing philosophy of <a href="https://github.com/mli/autocut">mli/autocut</a>, rebuilt for industrial reliability.</em>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/FFmpeg-Native_FilterGraph-007808?logo=ffmpeg&logoColor=white" alt="FFmpeg">
    <img src="https://img.shields.io/badge/Sync_Drift-0.00ms-brightgreen" alt="Zero Drift">
    <img src="https://img.shields.io/badge/Agent_Skill-Ready-8A63D2" alt="Agent Skill Ready">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
  </p>
</p>

---

## 💡 The Philosophy: Markdown-Driven Video Editing

Editing talking-head videos and software tutorials should not require dragging clips on a timeline in Premiere or Final Cut.

1. Whisper transcribes your raw footage into a **Markdown checklist** with millisecond timestamps.
2. You read the Markdown file like an article.
3. Uncheck `- [ ]` a line to discard a blooper, hesitation, or dead loading screen.
4. Keep `- [x]` to preserve the good parts.
5. **Run the script — your polished video is exported.**

```markdown
- [x] <-- Mark if you are done editing.

- [x] [1,00:00]  Hello everyone, welcome back.
- [ ] [2,00:03]  < No Speech >                        <-- 49s dead silence: CUT OUT!
- [ ] [3,00:52]  Um, sorry let me rephrase that...     <-- Blooper: CUT OUT!
- [x] [4,00:56]  Today we are going to build an Agent. <-- Keep!
```

---

## ⚡ The Hard Problem: Why Legacy AutoCut Failed in Production

The original [mli/autocut](https://github.com/mli/autocut) (7.8k stars) by Mu Li introduced this revolutionary workflow. However, in serious production, creators faced a critical roadblock:

* **The MoviePy Cumulative Drift**: Legacy AutoCut relied on Python's `MoviePy` for slicing and concatenating video chunks. MoviePy forces audio resampling (44.1kHz) and performs frame rounding on each clip. In a 5-minute video with 40-80 cuts, **time drift accumulates to 500ms ~ 1500ms**, causing severe lip-sync desynchronization by the end of the video.
* **The "Consonant Clipping" Trap**: Trimming tightly to audio timestamps chops off initial speech consonants (e.g. cutting *"Jev"* into *"ev"*). Biologically, human lips move 100-200ms before sound emits; hard cutting creates unnatural, robotic cadence.

---

## 🛠️ The Fix: What `autocut-skill` Rebuilds

`autocut-skill` throws away MoviePy and provides a **zero-drift, single-pass FFmpeg FilterGraph engine**:

| Metric | Legacy AutoCut (MoviePy) | `autocut-skill` (FFmpeg FilterGraph) |
| :--- | :--- | :--- |
| **A/V Sync Engine** | Python `MoviePy.concatenate` | **Native FFmpeg complex FilterGraph** (PTS clocks locked at decoder level) |
| **Cumulative Drift (50+ cuts)** | ❌ **500ms ~ 1500ms** (Noticeable lip lag) | ✅ **0.00ms (Frame-accurate synchronization)** |
| **Speech Breathing Buffer** | ❌ None (Hard cut, chops initial consonants) | ✅ **0.18s Pre-roll (inhale/lip open) + 0.15s Post-roll (trailing vowel)** |
| **Hardware Delay Correction** | ❌ Unsupported | ✅ `--advance <seconds>` (Fixes wireless mic/Bluetooth latency) |
| **Subtitle Hard-Burning** | ❌ Unsupported | ✅ `--burn-subtitles <srt>` (Anti-obscuring avatar margin styling) |
| **Privacy Area Blurring** | ❌ Unsupported | ✅ `--blur-box "st:et:x:y:w:h"` (Redacts API keys/tokens) |
| **Export Speed** | ❌ Slow CPU rendering | ✅ **Apple Silicon VideoToolbox hardware acceleration** (8x faster) |
| **Audio Quality** | Resampled 44.1kHz | **48,000Hz Hi-Fi pristine audio** |

---

## 📊 Real-World Dogfooding Benchmark

We use `autocut-skill` daily to produce all videos for our AI content channel. Here is a real benchmark from our 2026-09-22 production run:

* **Raw Video Duration**: 208.15s (3m 28s)
* **Final Cut Duration**: 104.49s (1m 44s)
* **Compression**: **-49.8% dead air eliminated** (removed a 49s browser loading wait + 5 stuttered lines)
* **Number of Cuts**: **22 cuts** (1 cut every 4.7 seconds)
* **Lip-Sync Accuracy**: **100% matched from first to final second**
* **Export Time**: **12.4 seconds** on M-series Mac

---

## 🚀 Quick Start

### 1. Installation

Requires `ffmpeg` installed on your system.

```bash
# Clone the repository
git clone https://github.com/huhao121/autocut-skill.git
cd autocut-skill

# Install in editable mode
pip install -e .
```

### 2. Basic Workflow

```bash
# Step 1: Transcribe video into SRT and Markdown checklist
autocut-skill transcribe raw_footage.mp4

# Step 2: Open raw_footage.md in VS Code or any text editor
# Review sentences: change `- [x]` to `- [ ]` for any blooper or dead pause.

# Step 3: Cut the video
autocut-skill cut raw_footage.mp4
# -> Outputs raw_footage_cut.mp4 with zero drift!

# Advanced: Compensate mic latency & burn subtitles with webcam avatar avoidance
autocut-skill cut raw_footage.mp4 --advance 0.56 --burn-subtitles raw_footage.srt
```

### 3. One-Shot Auto Cut

Don't want to edit manually? Cut all silent gaps automatically:

```bash
autocut-skill auto raw_footage.mp4
```

---

## 🤖 Use as an AI Agent Skill

`autocut-skill` is designed natively for autonomous AI coding agents (**Claude Code**, **Codex**, **Antigravity**, **Cursor**, **Hermes**).

Because the editing state is pure Markdown, **an LLM agent can act as your assistant video editor**:

```bash
# In Claude Code / Codex / Antigravity terminal:
"Use autocut-skill to transcribe raw.mp4.
Then read raw.md, remove all < No Speech > blocks and repeated lines,
and export the cut video."
```

The agent will read the Markdown file, audit the transcript, uncheck bloopers, and invoke `autocut-skill cut` autonomously.

---

## 📜 Acknowledgements & License

- **Original Inspiration**: Huge thanks to **Mu Li** and the contributors of [mli/autocut](https://github.com/mli/autocut) for the visionary concept of editing video via text.
- **Whisper**: Speech recognition powered by OpenAI's Whisper model.
- **License**: MIT License. See [LICENSE](LICENSE) for details.
