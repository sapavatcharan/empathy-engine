"""
Text-to-Speech engine with emotion-based vocal parameter modulation.
Maps detected emotion to rate (speed) and volume (amplitude).
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import pyttsx3

from emotion import EMOTION_POSITIVE, EMOTION_NEGATIVE, EMOTION_NEUTRAL, detect_emotion


# Baseline TTS parameters (neutral delivery)
DEFAULT_RATE = 175   # words per minute
DEFAULT_VOLUME = 0.9  # 0.0 to 1.0

# Emotion-to-voice mapping: (rate_offset, volume_offset) or multipliers
# Positive: slightly faster + fuller volume (enthusiastic)
# Negative: slower + slightly softer (calm, patient)
# Neutral: baseline
# We use rate deltas and volume scale so intensity can scale the effect.
EMOTION_TO_VOICE = {
    EMOTION_POSITIVE: {"rate_delta": 30, "volume_scale": 1.0},   # faster, full volume
    EMOTION_NEGATIVE: {"rate_delta": -40, "volume_scale": 0.85}, # slower, calmer
    EMOTION_NEUTRAL: {"rate_delta": 0, "volume_scale": 0.9},
}


def _get_vocal_parameters(emotion: str, intensity: float) -> Tuple[int, float]:
    """
    Map emotion and intensity to (rate, volume).
    Intensity scales the modulation so strong sentiment has a stronger effect.
    """
    config = EMOTION_TO_VOICE.get(emotion, EMOTION_TO_VOICE[EMOTION_NEUTRAL])
    rate_delta = config["rate_delta"]
    volume_scale = config["volume_scale"]

    # Scale by intensity (0..1) so "very happy" has more effect than "mildly happy"
    strength = 0.5 + 0.5 * intensity if intensity else 0.5
    rate = int(DEFAULT_RATE + rate_delta * strength)
    volume = min(1.0, max(0.3, volume_scale * (0.85 + 0.15 * strength)))

    return rate, volume


def synthesize(text: str, output_path: Optional[str] = None) -> Tuple[str, str, int, float]:
    """
    Analyze text emotion, modulate TTS parameters, and generate a WAV file.

    Args:
        text: Input text to speak.
        output_path: Optional path for the WAV file. If None, uses a temp file.

    Returns:
        Tuple of (path_to_wav_file, detected_emotion, rate_used, volume_used).
    """
    emotion, intensity = detect_emotion(text)
    rate, volume = _get_vocal_parameters(emotion, intensity)

    if not output_path:
        fd, output_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()

    return output_path, emotion, rate, volume
