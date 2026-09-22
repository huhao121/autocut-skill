"""
autocut-skill
A zero-drift, Markdown-driven video cut engine & Agent skill.
Inspired by mli/autocut, rewritten with native FFmpeg FilterGraph.
"""

__version__ = "0.1.0"
__author__ = "huhao121"

from .cutter import cut_video
from .transcribe import transcribe_video

__all__ = ["cut_video", "transcribe_video"]
