#!/usr/bin/env python3
"""
autocut-skill: Transcribe Engine
Transcribes speech in videos into millisecond-accurate SRT and Markdown checklists.
Driven 100% by native Whisper (CLI, openai-whisper, or faster-whisper).
"""

import os
import re
import shutil
import subprocess
import sys


def format_timestamp(seconds):
    """Format seconds into MM:SS format for Markdown display."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def srt_to_markdown(srt_path, md_path, auto_uncheck_silence=True):
    """Convert an SRT file into an AutoCut-compatible Markdown checklist."""
    with open(srt_path, "r", encoding="utf-8") as f:
        content = f.read()

    sub_pattern = re.compile(
        r"(\d+)\n(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n(.*?)(?=\n\d+\n|\Z)",
        re.DOTALL,
    )

    lines = [
        "- [x] <-- Mark if you are done editing.",
        "",
        f"Texts generated from [{os.path.basename(srt_path)}]({os.path.basename(srt_path)}).",
        "Mark the sentences with - [x] to keep, or - [ ] to cut out.",
        "",
    ]

    last_end = 0.0

    for m in sub_pattern.finditer(content):
        idx = int(m.group(1))
        sh, sm, ss, sms = map(int, m.groups()[1:5])
        eh, em, es, ems = map(int, m.groups()[5:9])
        st = sh * 3600 + sm * 60 + ss + sms / 1000.0
        et = eh * 3600 + em * 60 + es + ems / 1000.0
        text = m.group(10).strip().replace("\n", " ")

        # Detect silent gap > 2.0s
        if st - last_end > 2.0:
            lines.append(f"- [ ] [{idx-1 if idx>1 else 0},{format_timestamp(last_end)}]   < No Speech >")

        lines.append(f"- [x] [{idx},{format_timestamp(st)}]  {text}")
        last_end = et

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[+] Generated Markdown checklist: {md_path}")
    return True


def transcribe_video(video_path, output_dir=None, model="small"):
    """
    Transcribe a video to .srt and .md checklist using native Whisper.
    Supports system whisper CLI, openai-whisper, or faster-whisper.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    out_dir = output_dir or os.path.dirname(os.path.abspath(video_path))
    os.makedirs(out_dir, exist_ok=True)

    srt_path = os.path.join(out_dir, f"{base_name}.srt")
    md_path = os.path.join(out_dir, f"{base_name}.md")

    # Priority 1: Check if whisper CLI is installed (standard native Whisper)
    whisper_bin = shutil.which("whisper")
    if whisper_bin:
        print(f"[*] Found system whisper at: {whisper_bin}. Running transcription...")
        cmd = [
            whisper_bin,
            video_path,
            "--model", model,
            "--output_format", "srt",
            "--output_dir", out_dir,
        ]
        proc = subprocess.run(cmd)
        if proc.returncode == 0 and os.path.exists(srt_path):
            srt_to_markdown(srt_path, md_path)
            return srt_path, md_path

    # Priority 2: Try Python openai-whisper / faster-whisper library
    try:
        import whisper
        print(f"[*] Loading Python whisper model: {model}...")
        w_model = whisper.load_model(model)
        result = w_model.transcribe(video_path)

        # Write SRT
        lines = []
        for i, seg in enumerate(result["segments"], 1):
            st = seg["start"]
            et = seg["end"]
            text = seg["text"].strip()

            sh = int(st // 3600)
            sm = int((st % 3600) // 60)
            ss = int(st % 60)
            sms = int((st - int(st)) * 1000)

            eh = int(et // 3600)
            em = int((et % 3600) // 60)
            es = int(et % 60)
            ems = int((et - int(et)) * 1000)

            lines.append(f"{i}")
            lines.append(f"{sh:02d}:{sm:02d}:{ss:02d},{sms:03d} --> {eh:02d}:{em:02d}:{es:02d},{ems:03d}")
            lines.append(text)
            lines.append("")

        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        srt_to_markdown(srt_path, md_path)
        return srt_path, md_path
    except ImportError:
        pass

    # Priority 3: Try Python faster-whisper library if installed
    try:
        from faster_whisper import WhisperModel
        print(f"[*] Loading faster-whisper model: {model}...")
        fw_model = WhisperModel(model, device="auto", compute_type="auto")
        segments_gen, _ = fw_model.transcribe(video_path)

        lines = []
        for i, seg in enumerate(segments_gen, 1):
            st = seg.start
            et = seg.end
            text = seg.text.strip()

            sh = int(st // 3600)
            sm = int((st % 3600) // 60)
            ss = int(st % 60)
            sms = int((st - int(st)) * 1000)

            eh = int(et // 3600)
            em = int((et % 3600) // 60)
            es = int(et % 60)
            ems = int((et - int(et)) * 1000)

            lines.append(f"{i}")
            lines.append(f"{sh:02d}:{sm:02d}:{ss:02d},{sms:03d} --> {eh:02d}:{em:02d}:{es:02d},{ems:03d}")
            lines.append(text)
            lines.append("")

        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        srt_to_markdown(srt_path, md_path)
        return srt_path, md_path

    except ImportError:
        pass

    raise RuntimeError(
        "No Whisper transcription engine found.\n"
        "Please install Whisper to enable auto transcription:\n"
        "  pip install openai-whisper\n"
        "  (or: pip install faster-whisper)\n"
        "Note: video cutting (autocut-skill cut) does not require Whisper, only FFmpeg!"
    )
