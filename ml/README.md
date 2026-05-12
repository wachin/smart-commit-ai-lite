# Lightweight ML Engine

This directory contains the optional scikit-learn Conventional Commit type predictor.

It is offline-first and Debian-friendly:

```bash
sudo apt install python3-sklearn python3-joblib python3-langdetect python3-regex
python3 -m ml.train_model
```

The trainer reuses local examples from:

- `commit_examples_data/examples.json`
- `commit_examples_data/examples.db`
- `commit_examples_data/entries/`

It also adds a small built-in seed set so all supported labels are represented:
`feat`, `fix`, `docs`, `refactor`, `test`, and `chore`.

Generated artifacts:

- `ml/commit_model.pkl`
- `ml/vectorizer.pkl`

If either artifact is missing or cannot be loaded, the application falls back to
the existing `smart_commit_nltk.py` heuristic engine.

