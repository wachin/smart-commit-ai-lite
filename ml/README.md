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

Artifact policy:

- `ml/artifact_policy.py` defines the official distributed artifact paths.
- `ml/commit_model.pkl`, `ml/vectorizer.pkl`, and `ml/model_metadata.json`
  are the only tracked default artifact filenames.
- Local experiments should use different `.pkl` names under `ml/`; `.gitignore`
  keeps those experimental files out of the repository.
- `model_metadata.json` records `artifact_policy_version` so future artifact
  policy changes can be detected.

To train only from repository datasets, without built-in seed examples:

```bash
python3 -m ml.train_model --no-seed
```

To evaluate the local predictor against offline examples:

```bash
python3 -m ml.evaluate_model
```

Use `--json` for machine-readable output and `--no-seed` to evaluate only
repository datasets. If artifacts are missing, examples are counted as skipped.

Internal predictor interface:

- `ml/interfaces.py` defines the minimal `CommitTypePredictor` protocol.
- Current implementation: `ml/predictor.py`.
- Future local engines should expose `predict(text, language=None)` and return
  an object with a `commit_type` field.

Regenerate `commit_model.pkl`, `vectorizer.pkl`, and `model_metadata.json` when:

- new balanced examples are added to `commit_examples_data/`
- preprocessing behavior changes in `utils/preprocessing.py`
- supported labels or model metadata format changes
- Debian package validation is being prepared for release

The official distributed artifacts should use the default command with seed
examples enabled until the real dataset covers all supported labels well enough
on its own.
