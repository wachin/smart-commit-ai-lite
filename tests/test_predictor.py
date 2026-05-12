import tempfile
import unittest
from pathlib import Path

from ml.predictor import SklearnCommitPredictor


class SklearnPredictorTests(unittest.TestCase):
    def test_missing_model_returns_none_instead_of_failing(self):
        with tempfile.TemporaryDirectory() as tmp:
            predictor = SklearnCommitPredictor(
                model_path=Path(tmp) / "missing-model.pkl",
                vectorizer_path=Path(tmp) / "missing-vectorizer.pkl",
            )

            self.assertFalse(predictor.available)
            self.assertIsNone(predictor.predict("fixed crash when opening audio files"))

    def test_status_reports_missing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            predictor = SklearnCommitPredictor(
                model_path=Path(tmp) / "missing-model.pkl",
                vectorizer_path=Path(tmp) / "missing-vectorizer.pkl",
            )

            status = predictor.status()

            self.assertFalse(status.ready)
            self.assertFalse(status.model_exists)
            self.assertFalse(status.vectorizer_exists)
            self.assertEqual(status.message, "missing model and vectorizer artifacts")


if __name__ == "__main__":
    unittest.main()
