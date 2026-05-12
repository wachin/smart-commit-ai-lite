import tempfile
import unittest
import json
from pathlib import Path

from ml.predictor import SklearnCommitPredictor
from ml.train_model import MODEL_FORMAT_VERSION


class SklearnPredictorTests(unittest.TestCase):
    def test_missing_model_returns_none_instead_of_failing(self):
        with tempfile.TemporaryDirectory() as tmp:
            predictor = SklearnCommitPredictor(
                model_path=Path(tmp) / "missing-model.pkl",
                vectorizer_path=Path(tmp) / "missing-vectorizer.pkl",
                metadata_path=Path(tmp) / "missing-metadata.json",
            )

            self.assertFalse(predictor.available)
            self.assertIsNone(predictor.predict("fixed crash when opening audio files"))

    def test_status_reports_missing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            predictor = SklearnCommitPredictor(
                model_path=Path(tmp) / "missing-model.pkl",
                vectorizer_path=Path(tmp) / "missing-vectorizer.pkl",
                metadata_path=Path(tmp) / "missing-metadata.json",
            )

            status = predictor.status()

            self.assertFalse(status.ready)
            self.assertFalse(status.model_exists)
            self.assertFalse(status.vectorizer_exists)
            self.assertFalse(status.metadata_exists)
            self.assertIsNone(status.metadata)
            self.assertEqual(status.message, "missing model and vectorizer artifacts")

    def test_load_metadata_accepts_current_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            metadata_path = Path(tmp) / "model_metadata.json"
            metadata_path.write_text(
                json.dumps(
                    {
                        "format_version": MODEL_FORMAT_VERSION,
                        "training_examples": 12,
                        "labels": {"feat": 8, "fix": 4},
                        "model_path": "ml/commit_model.pkl",
                        "vectorizer_path": "ml/vectorizer.pkl",
                        "trainer": "test trainer",
                    }
                ),
                encoding="utf-8",
            )
            predictor = SklearnCommitPredictor(metadata_path=metadata_path)

            metadata = predictor.load_metadata()

            self.assertIsNotNone(metadata)
            self.assertEqual(metadata["training_examples"], 12)

    def test_status_reports_invalid_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / "commit_model.pkl"
            vectorizer_path = Path(tmp) / "vectorizer.pkl"
            metadata_path = Path(tmp) / "model_metadata.json"
            model_path.write_text("placeholder", encoding="utf-8")
            vectorizer_path.write_text("placeholder", encoding="utf-8")
            metadata_path.write_text("{}", encoding="utf-8")
            predictor = SklearnCommitPredictor(
                model_path=model_path,
                vectorizer_path=vectorizer_path,
                metadata_path=metadata_path,
            )

            status = predictor.status()

            self.assertFalse(status.ready)
            self.assertTrue(status.metadata_exists)
            self.assertIsNone(status.metadata)
            self.assertIn("model metadata is invalid", status.message)


if __name__ == "__main__":
    unittest.main()
