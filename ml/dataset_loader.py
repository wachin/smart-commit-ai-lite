"""Load local Conventional Commit examples for offline sklearn training."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from utils.regex_utils import regex


SUPPORTED_TYPES = {"feat", "fix", "docs", "refactor", "test", "chore"}
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TrainingExample:
    text: str
    label: str
    source: str


SEED_EXAMPLES = [
    ("added MIDI karaoke support", "feat"),
    ("implemented language detection for Spanish summaries", "feat"),
    ("fixed crash when opening audio files", "fix"),
    ("corrige error al abrir archivos de audio", "fix"),
    ("updated installation instructions", "docs"),
    ("documenta nuevas opciones de instalacion", "docs"),
    ("cleaned deprecated code paths", "refactor"),
    ("refactoriza el parser para separar responsabilidades", "refactor"),
    ("added regression tests for commit prediction", "test"),
    ("añade pruebas para el predictor de commits", "test"),
    ("updated build scripts and dependency notes", "chore"),
    ("actualiza tareas de mantenimiento del repositorio", "chore"),
]


def label_from_subject(subject: str) -> str | None:
    match = regex.match(r"\s*([a-z]+)(?:\(|:)", subject or "")
    if not match:
        return None
    label = match.group(1).lower()
    return label if label in SUPPORTED_TYPES else None


def _entry_to_example(entry: dict, source: str) -> TrainingExample | None:
    label = label_from_subject(entry.get("expected_subject", ""))
    text = (entry.get("original_text") or "").strip()
    if not label or not text:
        return None
    return TrainingExample(text=text, label=label, source=source)


def load_examples_json(path: Path | None = None) -> list[TrainingExample]:
    path = path or ROOT / "commit_examples_data" / "examples.json"
    if not path.exists():
        return []
    entries = json.loads(path.read_text(encoding="utf-8"))
    return [ex for entry in entries if (ex := _entry_to_example(entry, str(path)))]


def load_examples_db(path: Path | None = None) -> list[TrainingExample]:
    path = path or ROOT / "commit_examples_data" / "examples.db"
    if not path.exists():
        return []
    examples: list[TrainingExample] = []
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        for row in conn.execute("SELECT original_text, expected_subject FROM examples"):
            entry = dict(row)
            if ex := _entry_to_example(entry, str(path)):
                examples.append(ex)
    return examples


def load_entry_files(path: Path | None = None) -> list[TrainingExample]:
    path = path or ROOT / "commit_examples_data" / "entries"
    if not path.exists():
        return []
    examples = []
    for entry_path in sorted(path.glob("*.json")):
        entry = json.loads(entry_path.read_text(encoding="utf-8"))
        if ex := _entry_to_example(entry, str(entry_path)):
            examples.append(ex)
    return examples


def load_seed_examples() -> list[TrainingExample]:
    return [TrainingExample(text=text, label=label, source="built-in-seed") for text, label in SEED_EXAMPLES]


def load_training_examples(include_seed: bool = True) -> list[TrainingExample]:
    """Load and de-duplicate all offline training examples."""
    candidates = []
    candidates.extend(load_examples_json())
    candidates.extend(load_examples_db())
    candidates.extend(load_entry_files())
    if include_seed:
        candidates.extend(load_seed_examples())

    unique: list[TrainingExample] = []
    seen = set()
    for example in candidates:
        key = (regex.sub(r"\s+", " ", example.text.lower()).strip(), example.label)
        if key not in seen:
            unique.append(example)
            seen.add(key)
    return unique


def as_training_arrays(examples: list[TrainingExample]) -> tuple[list[str], list[str]]:
    return [example.text for example in examples], [example.label for example in examples]

