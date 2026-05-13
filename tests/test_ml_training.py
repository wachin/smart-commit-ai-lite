import importlib.util
import tempfile
import unittest
from pathlib import Path

from ml.dataset_loader import (
    SUPPORTED_TYPES,
    TrainingExample,
    label_from_subject,
    load_training_examples,
    summarize_label_balance,
)
from ml.train_model import MODEL_FORMAT_VERSION, build_metadata


class MLTrainingTests(unittest.TestCase):
    def test_dataset_loader_reuses_local_examples_and_seed_labels(self):
        examples = load_training_examples(include_seed=True)
        labels = {example.label for example in examples}
        dataset_only_labels = {example.label for example in load_training_examples(include_seed=False)}

        self.assertGreaterEqual(len(examples), 12)
        self.assertTrue(SUPPORTED_TYPES.issubset(labels))
        self.assertTrue(SUPPORTED_TYPES.issubset(dataset_only_labels))
        self.assertEqual(label_from_subject("feat(ui): add control"), "feat")
        self.assertEqual(label_from_subject("docs: update readme"), "docs")

    def test_build_metadata_describes_training_artifacts(self):
        metadata = build_metadata(
            example_count=12,
            label_counts={"feat": 8, "fix": 4},
            model_path=Path("ml/commit_model.pkl"),
            vectorizer_path=Path("ml/vectorizer.pkl"),
            label_balance={"largest_label": "feat", "imbalance_ratio": 2.0},
            seed_examples_included=False,
        )

        self.assertEqual(metadata["format_version"], MODEL_FORMAT_VERSION)
        self.assertEqual(metadata["training_examples"], 12)
        self.assertEqual(metadata["labels"], {"feat": 8, "fix": 4})
        self.assertEqual(metadata["label_balance"]["largest_label"], "feat")
        self.assertEqual(metadata["label_balance"]["imbalance_ratio"], 2.0)
        self.assertFalse(metadata["seed_examples_included"])
        self.assertEqual(metadata["model_path"], "ml/commit_model.pkl")
        self.assertEqual(metadata["vectorizer_path"], "ml/vectorizer.pkl")
        self.assertIn("LinearSVC", metadata["trainer"])

    def test_summarize_label_balance_reports_dataset_skew(self):
        examples = [
            TrainingExample("add feature", "feat", "test"),
            TrainingExample("add another feature", "feat", "test"),
            TrainingExample("fix crash", "fix", "test"),
            TrainingExample("update docs", "docs", "test"),
        ]

        summary = summarize_label_balance(examples)

        self.assertEqual(summary["total"], 4)
        self.assertEqual(summary["counts"]["feat"], 2)
        self.assertEqual(summary["counts"]["fix"], 1)
        self.assertEqual(summary["counts"]["chore"], 0)
        self.assertEqual(summary["largest_label"], "feat")
        self.assertEqual(summary["imbalance_ratio"], 2.0)

    def test_seed_examples_are_optional_training_support(self):
        without_seed = load_training_examples(include_seed=False)
        with_seed = load_training_examples(include_seed=True)

        self.assertGreaterEqual(len(with_seed), len(without_seed))
        self.assertFalse(any(example.source == "built-in-seed" for example in without_seed))
        self.assertTrue(any(example.source == "built-in-seed" for example in with_seed))

    @unittest.skipUnless(importlib.util.find_spec("sklearn"), "python3-sklearn is not installed")
    def test_training_writes_model_and_vectorizer(self):
        from ml.train_model import train

        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / "commit_model.pkl"
            vectorizer_path = Path(tmp) / "vectorizer.pkl"
            metadata_path = Path(tmp) / "model_metadata.json"
            stats = train(
                model_path=model_path,
                vectorizer_path=vectorizer_path,
                metadata_path=metadata_path,
            )

            self.assertTrue(model_path.exists())
            self.assertTrue(vectorizer_path.exists())
            self.assertTrue(metadata_path.exists())
            self.assertGreaterEqual(stats["training_examples"], 12)


if __name__ == "__main__":
    unittest.main()
