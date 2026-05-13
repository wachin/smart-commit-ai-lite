"""Offline language helpers for English and Spanish commit summaries."""

from __future__ import annotations

from utils.regex_utils import regex


SUPPORTED_LANGUAGES = {"en", "es"}

SPANISH_MARKERS = (
    " el ", " la ", " los ", " las ", " un ", " una ", " este ", " esta ",
    " que ", " para ", " con ", " sin ", " desde ", " hasta ", " también ",
    " he ", " hemos ", " creado", " añad", " agreg", " actualiz", " correg",
    " mejora", " incluye", " resume", " documento", " funcionalidades",
    " completadas", " pendientes", " pruebas", " multilenguaje",
    " le ", " metí", " puse", " arregló", " quedó",
)
ENGLISH_MARKERS = (
    " the ", " a ", " an ", " this ", " that ", " with ", " without ",
    " from ", " to ", " also ", " i ", " we ", " created", " added",
    " updated", " fixed", " improved", " includes", " document",
    " completed", " pending", " tests", " multilingual",
)


def language_signal_text(text: str) -> str:
    """Remove snippets that should not vote in language detection."""
    signal_lines = []
    in_fence = False

    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if regex.search(r"^\s*git\s+commit\b", line):
            continue
        signal_lines.append(raw_line)

    signal = "\n".join(signal_lines)
    signal = regex.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", signal)
    signal = regex.sub(r"`[^`]+`", " ", signal)
    return signal


def detect_language(text: str) -> str:
    """Detect English/Spanish input with deterministic rules and langdetect fallback."""
    cleaned = language_signal_text(text).strip()
    if not cleaned:
        return "en"

    lowered = f" {cleaned.lower()} "
    spanish_score = sum(2 for marker in SPANISH_MARKERS if marker in lowered)
    english_score = sum(2 for marker in ENGLISH_MARKERS if marker in lowered)
    spanish_score += len(regex.findall(r"[áéíóúñü¿¡]", lowered)) * 3

    if spanish_score != english_score:
        return "es" if spanish_score > english_score else "en"

    try:
        from langdetect import DetectorFactory, detect

        DetectorFactory.seed = 0
        detected = detect(cleaned)
        if detected in SUPPORTED_LANGUAGES:
            return detected
    except Exception:
        pass

    return "en"
