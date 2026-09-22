---
name: autocut-skill
description: "A zero-drift, Markdown-driven video cut engine & Agent skill. Transcribes speech into a Markdown checklist with millisecond timestamps, and cuts videos using native FFmpeg FilterGraph based on marked sentences. Eliminates MoviePy cumulative A/V sync drift and audio clipping with breathing buffers."
---

# autocut-skill

Edit video by writing Markdown. Built for creators and autonomous AI agents.

## When to use

- User says "cut this video", "remove silences and bloopers", "transcribe and cut"
- Editing talking-head videos, software tutorials, or screencasts without touching a timeline editor (PR/Final Cut/CapCut)
- Autonomous Agent editing pipeline: an Agent can audit the transcribed Markdown checklist, uncheck bloopers or `< No Speech >` dead pauses, and produce a finished cut video.

## Features

1. **Zero-Drift Sync**: Replaces legacy MoviePy with native FFmpeg single-graph FilterGraph. Audio and video PTS clocks are locked at the decoder level. 0.00ms drift across 100+ cuts.
2. **Breathing Buffers**: Automatic `0.18s` pre-roll (lips opening / initial consonants) and `0.15s` post-roll (trailing vowels). No chopped consonants (e.g. preserves "Jev" instead of clipping to "ev").
3. **Hardware Compensation**: Supports `--advance <seconds>` to offset Bluetooth/wireless microphone latency.
4. **Apple Silicon Acceleration**: Automatic `h264_videotoolbox` hardware encoding with 48,000Hz hi-fi audio.

## Commands

```bash
# Step 1: Transcribe video to SRT and Markdown checklist
autocut-skill transcribe video.mp4

# Step 2: Edit the generated video.md checklist:
# Keep sentence:   - [x] [1,00:00] Text to keep
# Discard pause:   - [ ] [2,00:15] < No Speech >

# Step 3: Cut video with millisecond accuracy
autocut-skill cut video.mp4

# One-shot mode: transcribe and automatically remove silence gaps
autocut-skill auto video.mp4
```
