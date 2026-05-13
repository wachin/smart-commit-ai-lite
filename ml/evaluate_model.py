"""Evaluate the local commit-type predictor against offline examples."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from typing import Protocol

from ml.dataset_loader import TrainingExample, load_training_examples
from ml.predictor import PredictionResult, SklearnCommitPredictor


class CommitTypePredictor(Protocol):
    def predict(self, text: str, language: str | None = None) -> PredictionResult | None:
        ...


@dataclass(frozen=True)
class EvaluationResult:
    total_examples: int
    evaluated_examples: int
    skipped_examples: int
    correct_predictions: int
    accuracy: float | None
    expected_labels: dict[str, int]
    predicted_labels: dict[str, int]


def evaluate_predictor(
    examples: list[TrainingExample],
    predictor: CommitTypePredictor,
) -> EvaluationResult:
    expected_counts = Counter(example.label for example in examples)
    predicted_counts: Counter[str] = Counter()
    correct = 0
    evaluated = 0

    for example in examples:
        prediction = predictor.predict(example.text)
        if prediction is None:
            continue
        evaluated += 1
        predicted_counts[prediction.commit_type] += 1
        if prediction.commit_type == example.label:
            correct += 1

    skipped = len(examples) - evaluated
    accuracy = round(correct / evaluated, 4) if evaluated else None
    return EvaluationResult(
        total_examples=len(examples),
        evaluated_examples=evaluated,
        skipped_examples=skipped,
        correct_predictions=correct,
        accuracy=accuracy,
        expected_labels=dict(sorted(expected_counts.items())),
        predicted_labels=dict(sorted(predicted_counts.items())),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the offline sklearn commit predictor.")
    parser.add_argument("--no-seed", action="store_true", help="Evaluate only repository datasets.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    examples = load_training_examples(include_seed=not args.no_seed)
    result = evaluate_predictor(examples, SklearnCommitPredictor())

    payload = {
        "total_examples": result.total_examples,
        "evaluated_examples": result.evaluated_examples,
        "skipped_examples": result.skipped_examples,
        "correct_predictions": result.correct_predictions,
        "accuracy": result.accuracy,
        "expected_labels": result.expected_labels,
        "predicted_labels": result.predicted_labels,
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"Total examples: {result.total_examples}")
        print(f"Evaluated examples: {result.evaluated_examples}")
        print(f"Skipped examples: {result.skipped_examples}")
        print(f"Correct predictions: {result.correct_predictions}")
        print(f"Accuracy: {result.accuracy if result.accuracy is not None else 'n/a'}")
        print(f"Expected labels: {result.expected_labels}")
        print(f"Predicted labels: {result.predicted_labels}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
