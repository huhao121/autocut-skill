#!/usr/bin/env python3
"""
autocut-skill CLI
Unified Command-Line Interface for autocut-skill.
"""

import argparse
import os
import sys
from .cutter import cut_video
from .transcribe import transcribe_video

BANNER = r"""
   ___        __        _____      __     _____ __   _ ____
  /   | __  __/ /_____ / ___/_  __/ /_   / ___// /__(_) / /
 / /| |/ / / / __/ __ \\__ \/ / / / __/   \__ \/ //_/ / / / 
/ ___ / /_/ / /_/ /_/ /__/ / /_/ / /_    ___/ / ,< / / / /  
/_/  |_\__,_/\__/\____/____/\__,_/\__/   /____/_/|_/_/_/_/   
                                      FFmpeg Zero-Drift Engine
"""


def main():
    parser = argparse.ArgumentParser(
        description="autocut-skill: Zero-drift Markdown video cut engine & Agent skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  autocut-skill transcribe raw.mp4\n"
               "  autocut-skill cut raw.mp4 --md raw.md --out cut.mp4\n"
               "  autocut-skill cut raw.mp4  (auto-detects raw.srt and raw.md)\n"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: transcribe
    p_trans = subparsers.add_parser("transcribe", help="Transcribe speech to SRT and Markdown checklist")
    p_trans.add_argument("video", help="Path to input video file")
    p_trans.add_argument("--model", default="small", help="Whisper model (tiny/base/small/medium/large)")
    p_trans.add_argument("--outdir", default=None, help="Output directory for .srt and .md")

    # Command: cut
    p_cut = subparsers.add_parser("cut", help="Cut video using Markdown checklist and native FFmpeg FilterGraph")
    p_cut.add_argument("video", help="Path to raw video file")
    p_cut.add_argument("--srt", default=None, help="Path to .srt file (defaults to <video_name>.srt)")
    p_cut.add_argument("--md", default=None, help="Path to .md checklist (defaults to <video_name>.md)")
    p_cut.add_argument("--out", default=None, help="Path to output video (defaults to <video_name>_cut.mp4)")
    p_cut.add_argument("--pre-roll", type=float, default=0.18, help="Pre-speech buffer in seconds (default: 0.18s)")
    p_cut.add_argument("--post-roll", type=float, default=0.15, help="Post-speech buffer in seconds (default: 0.15s)")
    p_cut.add_argument("--merge-gap", type=float, default=0.35, help="Merge sentences closer than this (default: 0.35s)")
    p_cut.add_argument("--advance", type=float, default=0.0, help="Audio advance hardware compensation in seconds")
    p_cut.add_argument("--bitrate", default="5500k", help="Output video bitrate (default: 5500k)")

    # Command: auto (transcribe + cut non-speech)
    p_auto = subparsers.add_parser("auto", help="One-shot: transcribe and automatically cut silent pauses")
    p_auto.add_argument("video", help="Path to input video file")
    p_auto.add_argument("--model", default="small", help="Whisper model")
    p_auto.add_argument("--out", default=None, help="Output video path")

    args = parser.parse_args()

    if not args.command:
        print(BANNER)
        parser.print_help()
        sys.exit(0)

    if args.command == "transcribe":
        transcribe_video(args.video, output_dir=args.outdir, model=args.model)

    elif args.command == "cut":
        video_dir = os.path.dirname(os.path.abspath(args.video))
        base_name = os.path.splitext(os.path.basename(args.video))[0]

        srt_path = args.srt or os.path.join(video_dir, f"{base_name}.srt")
        md_path = args.md or os.path.join(video_dir, f"{base_name}.md")
        out_path = args.out or os.path.join(video_dir, f"{base_name}_cut.mp4")

        success = cut_video(
            raw_video=args.video,
            srt_file=srt_path,
            md_file=md_path,
            output_file=out_path,
            pre_roll=args.pre_roll,
            post_roll=args.post_roll,
            merge_gap=args.merge_gap,
            audio_advance=args.advance,
            bitrate=args.bitrate,
        )
        if not success:
            sys.exit(1)

    elif args.command == "auto":
        print("[*] Step 1: Transcribing video and generating checklist...")
        srt_path, md_path = transcribe_video(args.video, model=args.model)
        
        video_dir = os.path.dirname(os.path.abspath(args.video))
        base_name = os.path.splitext(os.path.basename(args.video))[0]
        out_path = args.out or os.path.join(video_dir, f"{base_name}_cut.mp4")

        print("[*] Step 2: Cutting video based on speech segments...")
        success = cut_video(
            raw_video=args.video,
            srt_file=srt_path,
            md_file=md_path,
            output_file=out_path,
        )
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
