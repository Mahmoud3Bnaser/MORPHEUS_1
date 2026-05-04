"""
MORPHEUS-X Static Malware DNA Engine
Module: entropy.py

This module provides entropy calculation utilities used to detect
packed, compressed, encrypted, or obfuscated regions inside files.

Entropy is measured on a 0.0 to 8.0 scale for byte data.
Higher entropy often indicates packed or encrypted content.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Dict, Union


EntropyResult = Dict[str, Union[float, str, bool]]


LOW_ENTROPY_THRESHOLD = 4.5
MEDIUM_ENTROPY_THRESHOLD = 6.7
HIGH_ENTROPY_THRESHOLD = 7.2


def calculate_entropy(data: bytes) -> float:
    """
    Calculate Shannon entropy for a bytes object.

    Entropy range for byte data:
        0.0 = no randomness
        8.0 = maximum randomness

    Args:
        data: Raw bytes to analyze.

    Returns:
        Entropy value rounded to 4 decimal places.
    """
    if not data:
        return 0.0

    byte_counts = Counter(data)
    data_length = len(data)

    entropy = 0.0

    for count in byte_counts.values():
        probability = count / data_length
        entropy -= probability * math.log2(probability)

    return round(entropy, 4)


def classify_entropy(entropy: float) -> str:
    """
    Classify entropy value into a readable risk level.

    Args:
        entropy: Entropy value.

    Returns:
        Human-readable entropy classification.
    """
    if entropy < LOW_ENTROPY_THRESHOLD:
        return "low"
    if entropy < MEDIUM_ENTROPY_THRESHOLD:
        return "medium"
    if entropy < HIGH_ENTROPY_THRESHOLD:
        return "high"
    return "very_high"


def is_suspicious_entropy(entropy: float) -> bool:
    """
    Decide whether entropy is suspicious.

    Args:
        entropy: Entropy value.

    Returns:
        True if entropy suggests packing, compression, encryption, or obfuscation.
    """
    return entropy >= MEDIUM_ENTROPY_THRESHOLD


def analyze_entropy(data: bytes) -> EntropyResult:
    """
    Calculate and classify entropy for raw bytes.

    Args:
        data: Raw bytes to analyze.

    Returns:
        Dictionary containing entropy value, classification, and suspicious flag.
    """
    entropy = calculate_entropy(data)
    classification = classify_entropy(entropy)

    return {
        "entropy": entropy,
        "classification": classification,
        "suspicious": is_suspicious_entropy(entropy),
    }