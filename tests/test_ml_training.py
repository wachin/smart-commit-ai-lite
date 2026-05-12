import importlib.util
import tempfile
import unittest
from pathlib import Path

from ml.dataset_loader import SUPPORTED_TYPES, label_from_subject, load_training_examples


class MLTrainingTests(unittest.TestCase):
    def test_dataset_loader_reuses_local_examples_and_seed_labels(self):
        examples = load_training_examples(include_seed=True)
        labels = {example.label for example in examples}

        self.assertGreaterEqual(len(examples), 12)
        self.assertTrue(SUPPORTED_TYPES.issubset(labels))
        self.assertEqual(label_from_subject("feat(ui): add control"), "feat")
        self.assertEqual(label_from_subject("docs: update readme"), "docs")

    @unittest.skipUnless(importlib.util.find_spec("sklearn"), "python3-sklearn is not installed")
    def test_training_writes_model_and_vectorizer(self):
        from ml.train_model import train

        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / "commit_model.pkl"
            vectorizer_path = Path(tmp) / "vectorizer.pkl"
            stats = train(model_path=model_path, vectorizer_path=vectorizer_path)

            self.assertTrue(model_path.exists())
            self.assertTrue(vectorizer_path.exists())
            self.assertGreaterEqual(stats["examples"], 12)


if __name__ == "__main__":
    unittest.main()
