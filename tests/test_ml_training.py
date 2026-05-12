import importlib.util
import tempfile
import unittest
from pathlib import Path

from ml.dataset_loader import SUPPORTED_TYPES, label_from_subject, load_training_examples
from ml.train_model import MODEL_FORMAT_VERSION, build_metadata


class MLTrainingTests(unittest.TestCase):
    def test_dataset_loader_reuses_local_examples_and_seed_labels(self):
        examples = load_training_examples(include_seed=True)
        labels = {example.label for example in examples}

        self.assertGreaterEqual(len(examples), 12)
        self.assertTrue(SUPPORTED_TYPES.issubset(labels))
        self.assertEqual(label_from_subject("feat(ui): add control"), "feat")
        self.assertEqual(label_from_subject("docs: update readme"), "docs")

    def test_build_metadata_describes_training_artifacts(self):
        metadata = build_metadata(
            example_count=12,
            label_counts={"feat": 8, "fix": 4},
            model_path=Path("ml/commit_model.pkl"),
            vectorizer_path=Path("ml/vectorizer.pkl"),
        )

        self.assertEqual(metadata["format_version"], MODEL_FORMAT_VERSION)
        self.assertEqual(metadata["training_examples"], 12)
        self.assertEqual(metadata["labels"], {"feat": 8, "fix": 4})
        self.assertEqual(metadata["model_path"], "ml/commit_model.pkl")
        self.assertEqual(metadata["vectorizer_path"], "ml/vectorizer.pkl")
        self.assertIn("LinearSVC", metadata["trainer"])

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
