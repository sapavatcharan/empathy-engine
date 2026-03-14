"""
Emotion detection for the Empathy Engine.
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) to classify text
into Positive, Negative, or Neutral, with an optional intensity score.
"""

from __future__ import annotations

from typing import Tuple

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Emotional categories we support (at least 3 per requirements)
EMOTION_POSITIVE = "positive"
EMOTION_NEGATIVE = "negative"
EMOTION_NEUTRAL = "neutral"

# Thresholds for VADER compound score (-1 to 1)
POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05


def detect_emotion(text: str) -> Tuple[str, float]:
    """
    Analyze input text and classify into one of three emotions.

    Args:
        text: Raw input string to analyze.

    Returns:
        Tuple of (emotion_label, intensity).
        emotion_label: One of 'positive', 'negative', 'neutral'.
        intensity: Absolute strength of sentiment (0.0 to 1.0) for mapping to vocal modulation.
    """
    if not text or not text.strip():
        return EMOTION_NEUTRAL, 0.0

    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= POSITIVE_THRESHOLD:
        emotion = EMOTION_POSITIVE
        intensity = compound  # 0.05 to 1.0
    elif compound <= NEGATIVE_THRESHOLD:
        emotion = EMOTION_NEGATIVE
        intensity = abs(compound)  # 0.05 to 1.0
    else:
        emotion = EMOTION_NEUTRAL
        intensity = 0.0

    return emotion, intensity
