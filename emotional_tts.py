"""
Emotional TTS: natural, human-like speech with clear emotion.

Two backends (auto-selected):
1. ElevenLabs (best naturalness) – used when ELEVENLABS_API_KEY or ELEVEN_API_KEY is set.
2. Edge-TTS (free, no key) – uses a natural voice + strong prosody so emotion is audible.
"""

from __future__ import annotations

import asyncio
import os
from typing import Tuple

from emotion import EMOTION_NEGATIVE, EMOTION_NEUTRAL, EMOTION_POSITIVE, detect_emotion

# ---- ElevenLabs (optional): most natural, emotional ---- 
_ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel – calm, natural
_ELEVENLABS_MODEL = "eleven_multilingual_v2"   # emotionally expressive


def _synthesize_elevenlabs(text: str) -> Tuple[bytes, str, str, str]:
    """Use ElevenLabs for most natural, emotional speech. Requires API key."""
    from elevenlabs.client import ElevenLabs

    emotion, intensity = detect_emotion(text)
    # Lower stability = more expressive/emotional (ElevenLabs recommendation)
    stability = 0.35 if emotion != EMOTION_NEUTRAL else 0.55
    strength = 0.8 + 0.2 * intensity if intensity else 0.8
    stability = max(0.25, stability - (0.1 * strength))
    # Speed by emotion: positive faster, negative slower
    speed = 1.2 if emotion == EMOTION_POSITIVE else (0.88 if emotion == EMOTION_NEGATIVE else 1.0)
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", _ELEVENLABS_VOICE_ID)
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY"))
    out = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=_ELEVENLABS_MODEL,
        output_format="mp3_44100_128",
    )
    mp3_bytes = out if isinstance(out, bytes) else b"".join(out)
    rate_str = f"{int((speed - 1) * 100):+d}%"
    return mp3_bytes, emotion, rate_str, f"stability={stability:.2f}"


# ---- Edge-TTS (default): free, natural voice + strong prosody ----
import edge_tts  # noqa: E402

# Final default: Ryan (least robotic). Override with EDGE_TTS_VOICE in .env if needed.
EDGE_VOICE = os.environ.get("EDGE_TTS_VOICE", "en-GB-RyanNeural")

# Pitch by emotion: positive = higher, negative = lower (calm but not too slow), neutral = baseline
EMOTION_PROSODY = {
    EMOTION_POSITIVE: {"rate": "+40%", "pitch": "+18Hz", "volume": "+8%"},
    EMOTION_NEGATIVE: {"rate": "-12%", "pitch": "-14Hz", "volume": "-6%"},
    EMOTION_NEUTRAL: {"rate": "+0%", "pitch": "+0Hz", "volume": "+0%"},
}


def _get_prosody(emotion: str, intensity: float) -> Tuple[str, str, str]:
    p = EMOTION_PROSODY.get(emotion, EMOTION_PROSODY[EMOTION_NEUTRAL])
    strength = 0.75 + 0.25 * intensity if intensity else 0.75

    def scale_rate(s: str) -> str:
        if s == "+0%":
            return s
        sign = 1 if s.startswith("+") else -1
        val = int(s[1:-1]) * strength
        return f"{'+' if sign > 0 else '-'}{int(val)}%"

    def scale_pitch(s: str) -> str:
        if s == "+0Hz":
            return s
        sign = 1 if s.startswith("+") else -1
        val = int(s[1:-2]) * strength
        return f"{'+' if sign > 0 else '-'}{int(val)}Hz"

    return scale_rate(p["rate"]), scale_pitch(p["pitch"]), p["volume"]


async def _synthesize_edge_async(text: str) -> Tuple[bytes, str, str, str, str]:
    emotion, intensity = detect_emotion(text)
    rate, pitch, volume = _get_prosody(emotion, intensity)
    communicate = edge_tts.Communicate(
        text,
        EDGE_VOICE,
        rate=rate,
        pitch=pitch,
        volume=volume,
    )
    chunks = []
    async for chunk in communicate.stream():
        if isinstance(chunk, dict) and chunk.get("type") == "audio":
            chunks.append(chunk["data"])
    return b"".join(chunks), emotion, rate, pitch, volume


def _synthesize_edge(text: str) -> Tuple[bytes, str, str, str, str]:
    return asyncio.run(_synthesize_edge_async(text))


# ---- Public API ----
def synthesize_emotional(text: str) -> Tuple[bytes, str, str, str, str]:
    """
    Generate emotional speech (MP3). Uses ElevenLabs if API key is set,
    otherwise Edge-TTS with pitch/rate/volume by emotion.
    Returns (mp3_bytes, emotion, rate_display, pitch_display, volume_display).
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVEN_API_KEY")
    if api_key:
        try:
            mp3, em, rate, vol = _synthesize_elevenlabs(text)
            return mp3, em, rate, "+0Hz", vol  # ElevenLabs no pitch param
        except Exception:
            pass  # fallback to Edge
    return _synthesize_edge(text)
