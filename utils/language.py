"""Offline language helpers for English and Spanish commit summaries."""

from __future__ import annotations

from utils.regex_utils import regex


SUPPORTED_LANGUAGES = {"en", "es"}


def detect_language(text: str) -> str:
    """Detect English/Spanish input with langdetect plus a deterministic fallback."""
    cleaned = (text or "").strip()
    if not cleaned:
        return "en"

    try:
        from langdetect import DetectorFactory, detect

        DetectorFactory.seed = 0
        detected = detect(cleaned)
        if detected in SUPPORTED_LANGUAGES:
            return detected
    except Exception:
        pass

    lowered = f" {cleaned.lower()} "
    spanish_score = len(regex.findall(r"[áéíóúñü¿¡]", lowered)) * 3
    english_score = 0

    for marker in (" el ", " la ", " los ", " las ", " para ", " con ", " que ", " añadido", " agregado", " correg"):
        spanish_score += 2 if marker in lowered else 0
    for marker in (" the ", " a ", " an ", " with ", " for ", " fixed", " added", " updated", " changed"):
        english_score += 2 if marker in lowered else 0

    return "es" if spanish_score > english_score else "en"

