# Lightweight ML Engine

This directory contains the local scikit-learn Conventional Commit type predictor.

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
- `ml/model_metadata.json`

The metadata file records the model format version, training example count,
label counts, label-balance summary, artifact paths, and whether built-in seed
examples were included.

To train only from repository datasets, without built-in seed examples:

```bash
python3 -m ml.train_model --no-seed
```

Regenerate `commit_model.pkl`, `vectorizer.pkl`, and `model_metadata.json` when:

- new balanced examples are added to `commit_examples_data/`
- preprocessing behavior changes in `utils/preprocessing.py`
- supported labels or model metadata format changes
- Debian package validation is being prepared for release

The official distributed artifacts should use the default command with seed
examples enabled until the real dataset covers all supported labels well enough
on its own.
