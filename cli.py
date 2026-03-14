#!/usr/bin/env python3
"""
CLI for the Empathy Engine: accept text and produce emotion-modulated speech (WAV).
Usage:
  python cli.py "Your text here"
  python cli.py   # prompts for text interactively
"""

import sys
from pathlib import Path

# Ensure package root is on path when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent))

from tts_engine import synthesize


def main() -> None:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text to synthesize with emotional voice: ").strip()

    if not text:
        print("No text provided. Exiting.")
        sys.exit(1)

    out_path, emotion, rate, volume = synthesize(text)
    print(f"Emotion detected: {emotion}")
    print(f"Vocal parameters: rate={rate} wpm, volume={volume:.2f}")
    print(f"Audio saved to: {out_path}")
    print("Play the file with your system player or open the web UI for in-browser playback.")


if __name__ == "__main__":
    main()
