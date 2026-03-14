#!/usr/bin/env python3
"""
Run synthesis from a subprocess (so pyttsx3 has a proper environment).
Usage: python sync_runner.py <text_file> <output_wav> <output_meta>
Reads text from text_file, calls synthesize(), writes WAV to output_wav,
writes "emotion\\nrate\\nvolume" to output_meta.
"""

import sys
from pathlib import Path

# Run from project root so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tts_engine import synthesize


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(2)
    text_path, wav_path, meta_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        sys.exit(3)
    path, emotion, rate, volume = synthesize(text, wav_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"{emotion}\n{rate}\n{volume}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
