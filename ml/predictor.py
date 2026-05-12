"""Local sklearn predictor and artifact validation."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib

from ml.dataset_loader import SUPPORTED_TYPES
from utils.language import detect_language
from utils.preprocessing import preprocess_text


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = ROOT / "ml" / "commit_model.pkl"
DEFAULT_VECTORIZER_PATH = ROOT / "ml" / "vectorizer.pkl"


@dataclass(frozen=True)
class PredictionResult:
    commit_type: str
    confidence: float | None
    language: str
    engine: str = "sklearn"


@dataclass(frozen=True)
class ModelStatus:
    model_path: Path
    vectorizer_path: Path
    model_exists: bool
    vectorizer_exists: bool
    loadable: bool
    message: str

    @property
    def ready(self) -> bool:
        return self.model_exists and self.vectorizer_exists and self.loadable


class SklearnCommitPredictor:
    """Load local joblib artifacts and predict Conventional Commit types."""

    def __init__(
        self,
        model_path: Path | str = DEFAULT_MODEL_PATH,
        vectorizer_path: Path | str = DEFAULT_VECTORIZER_PATH,
    ) -> None:
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self._model: Any | None = None
        self._vectorizer: Any | None = None
        self._load_error: str | None = None

    @property
    def available(self) -> bool:
        return self.model_path.exists() and self.vectorizer_path.exists()

    def load(self) -> bool:
        if self._model is not None and self._vectorizer is not None:
            return True
        if not self.available:
            self._load_error = "model or vectorizer artifact is missing"
            return False
        try:
            self._model = joblib.load(self.model_path)
            self._vectorizer = joblib.load(self.vectorizer_path)
            self._load_error = None
            return True
        except Exception as exc:
            self._model = None
            self._vectorizer = None
            self._load_error = str(exc)
            return False

    def status(self, try_load: bool = False) -> ModelStatus:
        model_exists = self.model_path.exists()
        vectorizer_exists = self.vectorizer_path.exists()
        loadable = False

        if model_exists and vectorizer_exists:
            loadable = self.load() if try_load else True

        if not model_exists and not vectorizer_exists:
            message = "missing model and vectorizer artifacts"
        elif not model_exists:
            message = "missing model artifact"
        elif not vectorizer_exists:
            message = "missing vectorizer artifact"
        elif loadable:
            message = "model artifacts are ready"
        else:
            message = f"model artifacts could not be loaded: {self._load_error or 'unknown error'}"

        return ModelStatus(
            model_path=self.model_path,
            vectorizer_path=self.vectorizer_path,
            model_exists=model_exists,
            vectorizer_exists=vectorizer_exists,
            loadable=loadable,
            message=message,
        )

    def predict(self, text: str, language: str | None = None) -> PredictionResult | None:
        if not text or not text.strip() or not self.load():
            return None

        language = language if language in {"en", "es"} else detect_language(text)
        processed = preprocess_text(text, language)
        if not processed:
            return None

        try:
            features = self._vectorizer.transform([processed])
            label = str(self._model.predict(features)[0])
            if label not in SUPPORTED_TYPES:
                return None
            return PredictionResult(label, self._confidence(features, label), language)
        except Exception:
            return None

    def _confidence(self, features: Any, label: str) -> float | None:
        """Approximate confidence for LinearSVC using normalized margins."""
        if self._model is None or not hasattr(self._model, "decision_function"):
            return None
        try:
            scores = self._model.decision_function(features)
            classes = list(getattr(self._model, "classes_", []))
            if not classes:
                return None
            if len(classes) == 2 and not hasattr(scores[0], "__iter__"):
                score = float(scores[0])
                raw = score if classes[1] == label else -score
                return round(1.0 / (1.0 + math.exp(-raw)), 3)
            row = [float(value) for value in scores[0]]
            max_score = max(row)
            exps = [math.exp(min(50.0, value - max_score)) for value in row]
            total = sum(exps)
            if total <= 0:
                return None
            index = classes.index(label)
            return round(exps[index] / total, 3)
        except Exception:
            return None


def predict_commit_type(text: str, language: str | None = None) -> PredictionResult | None:
    return SklearnCommitPredictor().predict(text, language)
