# Roadmap: NLTK + Lightweight ML Git Commit Generator

This roadmap tracks the progress of the NLTK-based smart commit generator, now extended with an optional classic scikit-learn ML engine. The goal is to improve Conventional Commit prediction without turning the project into a heavy AI application: everything should stay local, lightweight, explainable, maintainable, and Debian 12 friendly.

## Project Contract

### Philosophy
- [x] Keep the project lightweight, offline-first, open source, Linux friendly, Debian 12 friendly, and low-resource friendly.
- [x] Prioritize stability, offline compatibility, Debian compatibility, low memory usage, and then accuracy.
- [x] Keep `smart_commit_nltk.py` functional as the existing heuristic engine.
- [x] Extend the current architecture instead of replacing it.
- [x] Avoid unnecessary complexity and heavy dependencies.

### Technical Boundaries
- [x] Do not use transformers, torch, tensorflow, spaCy, Hugging Face, neural networks, cloud APIs, LLM frameworks, online inference, or telemetry.
- [x] Use dependencies available in Debian 12 repositories: `python3-nltk`, `python3-sklearn`, `python3-joblib`, `python3-langdetect`, and `python3-regex`.
- [x] Keep `python3-gensim` optional, not required.
- [x] Do not depend on heavy pip-only packages for the main path.
- [x] Keep the application fully usable without internet access once local NLTK data and, if used, the local model are present.

### Engine Responsibilities
- [x] NLTK and local utilities: normalization, cleanup, tokenization, stemming, stopword removal, and preprocessing.
- [x] scikit-learn: TF-IDF vectorization, ML classification, and commit type prediction.
- [x] Existing heuristics: fallback, subject/body generation, scope detection, and compatibility with the current UI behavior.
- [x] `python3-langdetect`: support language detection when useful, with deterministic fallback behavior.
- [x] `python3-regex`: improve regular-expression handling where useful, with a cautious fallback if the package is missing.

### ML Objective
- [x] Predict Conventional Commit types from user text.
- [x] Support these types: `feat`, `fix`, `docs`, `refactor`, `test`, and `chore`.
- [x] Use `TfidfVectorizer` and `LinearSVC`.
- [x] Save the model locally with `joblib`.
- [x] Save the vectorizer separately.
- [x] Load quickly and fail without breaking the application.
- [x] Avoid online inference and external services.

## Current State

The program is already usable for daily work: it accepts pasted English or Spanish text, removes Markdown/command noise, detects language, proposes `type(scope)`, generates a localized subject and body, lets the user manually correct language/type/scope, and copies the command without a modal dialog.

The current improvement track is not Git integration. It is better semantic quality from pasted text. The ML layer must remain optional, classic, and local on top of the NLTK engine, not a replacement.

### Latest Important Progress
- [x] Removed the separate subject/body preview because it did not improve the workflow.
- [x] Added word-boundary-aware subject truncation.
- [x] Fixed prioritization so semantic changes are not hidden by secondary test or documentation mentions.
- [x] Added detection for indirect validation phrases such as `Result: 20 tests OK`, `full suite passes`, `py_compile`, `compileall`, `unittest`, and `pytest`.
- [x] Added file mention detection to classify code, tests, documentation, reports, and configuration.
- [x] Expanded the body from 5 to 7 bullets to preserve important details.
- [x] Added bullet ranking so main changes come first, tests/docs/reports follow, and validation stays last.
- [x] Added an optional ML architecture with scikit-learn, TF-IDF, LinearSVC, and fallback to NLTK heuristics.
- [x] Current suite: 26 registered tests, 25 passing, and 1 training test skipped when `python3-sklearn` is not installed.

### ML Prompt Compliance Status
- [x] `smart_commit_nltk.py` remains present and functional.
- [x] The sklearn engine is modular and optional.
- [x] The application works even if `ml/commit_model.pkl` and `ml/vectorizer.pkl` are missing.
- [x] Training reuses `commit_examples_data/examples.json`, `commit_examples_data/examples.db`, and `commit_examples_data/entries/`.
- [x] The predictor returns a type and approximate confidence when the model supports it.
- [x] The system supports English and Spanish input.
- [x] The project includes `ml/`, `utils/`, and dedicated tests for the new architecture.
- [x] `ml/*.pkl` artifacts are treated as locally generated files and are not versioned by default.
- [ ] Validate real training and predictions on Debian 12 with `python3-sklearn` installed.
- [ ] A pre-trained model will be distributed, and if the user wishes, they will have the instructions to train it locally as needed.

### Current Quality Example

Input summary:

```text
I improved file mention detection in pasted text.
I updated smart_commit_nltk.py, tests/test_smart_commit_nltk.py, README.md,
Roadmap.md, and commit_examples_data/comparison_report.json.
Result: 19 tests OK.
```

Current expected output:

```bash
git commit -m "feat(nlp): improve file mention detection" \
  -m "- Update code paths mentioned in the summary" \
  -m "- Cover changes with regression tests" \
  -m "- Update documentation mentioned in the summary" \
  -m "- Update evaluation data or reports" \
  -m "- Validation: 19 tests pass"
```

### Useful Commands

Install Debian dependencies:

```bash
sudo apt install \
    python3-pyqt6 \
    python3-nltk \
    python3-sklearn \
    python3-joblib \
    python3-langdetect \
    python3-regex
```

Optional dependency:

```bash
sudo apt install python3-gensim
```

Train or retrain the local ML model:

```bash
python3 -m ml.train_model
```

Run the regression suite:

```bash
QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -v
```

Recalculate the comparison report:

```bash
QT_QPA_PLATFORM=offscreen python3 commit_examples_data/compare_generator.py
```

Note: `__pycache__/smart_commit_nltk.cpython-311.pyc` may appear modified because it is already tracked by Git. `.gitignore` prevents new generated artifacts, but removing that tracked bytecode from the index remains pending.

## Completed Features

### [x] Initial Project Setup
- [x] Created the repository and basic structure.
- [x] Installed the main dependencies: NLTK and PyQt6.
- [x] Added startup checks for required NLTK data.
- [x] Added first-run download support for missing NLTK packages.
- [x] Documented Debian packages required for the optional ML engine.
- [x] Documented `python3-gensim` as an optional dependency.

### [x] Desktop Interface
- [x] Main PyQt6 window for pasting change summaries.
- [x] Button for generating commits with NLTK.
- [x] Button for clearing user input.
- [x] Detected-language indicator: pending, Spanish, or English.
- [x] Manual language selector: Automatic, Spanish, or English.
- [x] Manual selectors for type and scope before copying.
- [x] Non-intrusive warning when input contains heavy noise or code blocks.
- [x] Output area with multiline `git commit` command.
- [x] Button for copying the command to the clipboard.
- [x] Copy confirmation in the button itself, without a modal message.

### [x] Base NLTK Generator
- [x] Tokenization and POS tagging for English text.
- [x] Initial verb/object extraction for subject construction.
- [x] Sentence scoring to choose the most representative phrase.
- [x] Conventional Commit format: `type(scope): subject`.
- [x] Length limits for subjects and body lines.

### [x] Commit Example Dataset
- [x] Created `COMMIT_GENERATION_EXAMPLES.md` with real cases.
- [x] Created `parse_commit_examples.py` to parse examples.
- [x] Exported examples to JSON and SQLite.
- [x] Validated 45 processed entries.

### [x] Comparison and Evaluation System
- [x] Created `compare_generator.py`.
- [x] Compared generated commits against expected commits.
- [x] Produced a JSON report with similarity metrics.
- [x] Improved initial similarity from 0.453 to 0.528.
- [x] Later improved subject similarity to 0.509.
- [x] Updated `compare_generator.py` for the current bilingual signature.
- [x] Recalculated `comparison_report.json` after bilingual improvements.
- [x] Recorded current baseline: 45 examples, subject similarity 0.446, body ratio 0.000.

### [x] Noise Filtering
- [x] Removed terminal commands and irrelevant conversational phrases.
- [x] Cleaned lines generated by tools or assistants.
- [x] Filtered Markdown triple-backtick blocks.
- [x] Ignored pasted `git commit -m` commands inside summaries.
- [x] Ignored embedded `-m` lines to avoid polluting the body.
- [x] Cleaned Markdown links while preserving visible link text.
- [x] Preserved useful validations such as `py_compile` when they appear inside code blocks.

### [x] Bilingual English/Spanish Support
- [x] Simple input language detection (`es` / `en`).
- [x] Language-specific tokenization using English or Spanish Punkt.
- [x] Subject and body generation in the same language as the summary.
- [x] Support for common Spanish verbs: `creado`, `actualizado`, `incluye`, `resume`, `corrige`, and `mejora`.
- [x] Spanish object extraction through local linguistic rules.
- [x] Specific cases for roadmap summaries in English and Spanish.
- [x] Specific cases for bilingual/NLP improvements.

### [x] Type and Scope Detection
- [x] Automatic type detection: `feat`, `fix`, `docs`, `test`, `build`, `ci`, `style`, `refactor`, `perf`.
- [x] Automatic scope detection: `app`, `ui`, `docs`, `repo`, `dict`, `tools`, `nlp`.
- [x] Fixed false-positive `ci` detection inside words such as `funcionalidades` and `secciones`.
- [x] Prioritized NLP/bilingual changes as `feat(nlp)`.
- [x] Classified newly created roadmaps as `docs(repo)`.

### [x] Lightweight Optional ML Engine
- [x] Created `ml/dataset_loader.py` to reuse `examples.json`, `examples.db`, and `commit_examples_data/entries/`.
- [x] Created `ml/train_model.py` with `TfidfVectorizer` and `LinearSVC`.
- [x] Saved `commit_model.pkl` and `vectorizer.pkl` locally with `joblib`.
- [x] Created `ml/predictor.py` with fast loading and silent fallback to heuristics.
- [x] Added offline seed examples to cover `feat`, `fix`, `docs`, `refactor`, `test`, and `chore`.
- [x] Added shared utilities in `utils/` for NLTK preprocessing, language detection, and `python3-regex`.
- [x] Documented Debian installation, local training, and behavior without a model.
- [x] Started separating NLTK/preprocessing responsibilities from sklearn/classification responsibilities.
- [x] Added automatic fallback to the heuristic engine when ML prediction fails.

### [x] Offline and Extensible Architecture
- [x] Kept the existing heuristic engine as fallback.
- [x] Added the sklearn engine without breaking the current UI flow.
- [x] Prepared the structure for future engines: heuristic, sklearn, and possible future optional engines.
- [x] Avoided any dependency on network access, external APIs, telemetry, or online inference.
- [x] Kept model artifacts as local files generated by `joblib`.

### [x] Body Line Generation
- [x] Generated up to 7 relevant bullets.
- [x] Localized bullets in English or Spanish according to the input text.
- [x] Specific bullets for roadmap progress tracking.
- [x] Specific bullets for bilingual/NLP support.
- [x] Validation bullets for `compileall`, tests, and `py_compile`.
- [x] Basic deduplication to avoid repeated bullets.

### [x] Documentation
- [x] Updated README with current capabilities.
- [x] Added output examples in English and Spanish.
- [x] Updated Roadmap with completed and pending features.
- [x] Updated README with testing and evaluation commands.

### [x] Initial Evaluation and Testing
- [x] Created a `unittest` regression suite.
- [x] Tests for `strip_markdown_noise()`.
- [x] Tests for language detection.
- [x] Tests for bilingual `feat(nlp)` generation in Spanish and English.
- [x] Test for Spanish roadmap input as `docs(repo)`.
- [x] Test to avoid false-positive `ci` inside common words.
- [x] Test to prioritize testing/evaluation summaries over bilingual terms.
- [x] Test for clearing input, output, and copy button state.
- [x] Test to prioritize Clear Input summaries over test/Roadmap mentions.
- [x] Test to show and reset detected language in the interface.
- [x] Test to prioritize detected-language summaries over Roadmap mentions.
- [x] Test to manually force the generation language.
- [x] Test to manually edit type/scope and regenerate the command.
- [x] Test to prioritize type/scope summaries over test/Roadmap mentions.
- [x] Test to confirm copy state in the button without a modal message.
- [x] Test for noise warnings from code blocks and pasted commits.
- [x] Test for subject truncation without cutting words.
- [x] Test to prioritize preview removal and truncation summaries over test mentions.
- [x] Test to detect indirect validations such as `full suite passes: 18 tests OK`.
- [x] Test to detect code, test, documentation, and report mentions.
- [x] Test to rank bullets by importance and remove duplicate generic documentation.
- [x] Tests for dataset loading and predictor fallback when no model exists.
- [x] Unit tests for common Spanish action extraction.
- [x] Direct tests for `select_commit_type()` with core categories.
- [x] Direct tests for `detect_scope()` with common project areas.
- [x] Successful suite run: 25 tests pass and 1 is skipped without `python3-sklearn`.

### [x] Generated Artifact Hygiene
- [x] Created `.gitignore` entries for `__pycache__/` and `*.py[cod]`.

## Future Improvements

### Recommended Next Session
- [ ] Test the program with the latest Codex-generated summary and compare it against the commit a richer AI would produce.
- [ ] If the subject is too generic, add a specific subject rule before touching the body.
- [ ] If the body has good bullets but poor ordering, adjust `rank_body_lines()`.
- [ ] If useful information is lost from pasted text, inspect `clean_input()` first.
- [ ] After each improvement, add or adjust a regression test in `tests/test_smart_commit_nltk.py`.
- [ ] Always run `QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -v`.

### [ ] Evaluation and Testing
- [x] Add more unit tests for Spanish action extraction.
- [x] Add more unit tests for `select_commit_type()` and `detect_scope()`.
- [ ] Add ML prediction tests with a trained model when `python3-sklearn` is available.
- [ ] Test on Debian 12 with `python3-sklearn`, `python3-joblib`, `python3-langdetect`, and `python3-regex` installed from apt.
- [ ] Verify prompt examples: crash/audio -> `fix`, MIDI karaoke -> `feat`, instructions -> `docs`, deprecated code -> `refactor`.
- [ ] Add regression cases for mixed English/Spanish texts.
- [ ] Add regression cases for summaries with several modified files.
- [ ] Define new metrics that do not penalize the current 7-bullet limit.
- [ ] Improve historical dataset metrics without losing recent bilingual cases.

### [ ] ML Engine and Data
- [ ] Evaluate dataset balance: the historical examples currently favor `feat`.
- [ ] Add more real examples for `fix`, `docs`, `refactor`, `test`, and `chore`.
- [ ] Measure local model accuracy without increasing weight or complexity.
- [ ] Document when to regenerate `commit_model.pkl` and `vectorizer.pkl`.
- [ ] Keep offline seed examples only as support while the real dataset grows.

### [ ] Language Support
- [ ] Expand Spanish verbs and patterns.
- [ ] Improve language detection for mixed-language texts.
- [ ] Separate language-specific rules into more maintainable structures.
- [ ] Evaluate a Spanish POS tagger if more grammatical precision is desired.
- [ ] Support regional variants and more colloquial phrases.

### [ ] Architecture and Maintainability
- [x] Add external modules for preprocessing, language, and ML without rewriting `smart_commit_nltk.py`.
- [ ] Fully separate heuristic NLP logic from the PyQt6 interface.
- [ ] Create a dedicated class or module for input cleanup.
- [ ] Create a dedicated module for type/scope detection.
- [ ] Create reusable fixtures with real examples.
- [ ] Decide whether `ml/*.pkl` artifacts should be pre-trained and distributed or kept as local generated files.
- [ ] Define a common engine interface for `heuristic`, `sklearn`, and future optional engines.
- [ ] Remove any already-tracked `__pycache__` files from the Git index.

### [ ] User Interface
- [x] Allow manual language override.
- [x] Allow editing type/scope from the UI before copying.
- [x] Show warnings when input contains heavy noise or many code blocks.

### [ ] Commit Quality
- [x] Improve bullet ranking by importance.
- [x] Detect validations and tests even when they appear in indirect phrases.
- [x] Detect documentation, test, and code mentions inside pasted text.
- [x] Improve subject truncation so it does not cut words.
- [x] Expand the body up to 7 bullets to preserve relevant changes and validation.
- [x] Prioritize combined semantic improvements over secondary test/documentation mentions.
- [ ] Generate alternatives when several interpretations are possible.

---

**Last updated:** May 12, 2026  
**Status:** Functional for basic use and daily iteration. It now has initial regressions, dataset evaluation, and an optional offline ML engine. The next priority is improving semantic quality from pasted text without losing lightness or Debian compatibility.
