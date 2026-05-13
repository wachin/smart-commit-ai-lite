import os
import json
import re
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from PyQt6.QtWidgets import QApplication
from smart_commit_nltk import NLPCommitGenerator
JSON_PATH = ROOT / 'examples.json'
MAX_BODY_LINES = 7


def normalize_subject(subject: str) -> str:
    return subject.strip()


def format_diff(a: str, b: str) -> str:
    matcher = difflib.SequenceMatcher(None, a, b)
    return f'{matcher.ratio():.2f}'


def compare_entry(entry, generator):
    orig = entry['original_text']
    verb, obj, language = generator.analyze_with_nltk(orig)
    scope = generator.detect_scope(orig)
    commit_type = generator.select_commit_type(orig, verb, obj)
    subject_text = generator.format_subject(verb, obj, language)
    subject = f'{commit_type}({scope}): {subject_text}'
    if len(subject) > 50:
        subject = subject[:47] + '...'
    body_lines = generator.generate_body_lines(generator.clean_input(orig), language)

    expected_subject = entry['expected_subject']
    expected_body = entry['expected_body_lines']
    capped_expected_body = expected_body[:MAX_BODY_LINES]

    subject_match = subject == expected_subject
    body_count_match = len(body_lines) == len(expected_body)
    capped_body_count_match = len(body_lines) == len(capped_expected_body)
    subject_similarity = difflib.SequenceMatcher(None, subject, expected_subject).ratio()

    common = sum(1 for line in body_lines if line in expected_body)
    body_line_ratio = common / max(1, max(len(body_lines), len(expected_body)))
    capped_common = sum(1 for line in body_lines if line in capped_expected_body)
    capped_body_line_ratio = capped_common / max(1, max(len(body_lines), len(capped_expected_body)))
    capped_body_coverage = capped_common / max(1, len(capped_expected_body))

    return {
        'title': entry['title'],
        'expected_subject': expected_subject,
        'generated_subject': subject,
        'subject_match': subject_match,
        'subject_similarity': subject_similarity,
        'expected_body_count': len(expected_body),
        'capped_expected_body_count': len(capped_expected_body),
        'generated_body_count': len(body_lines),
        'body_count_match': body_count_match,
        'capped_body_count_match': capped_body_count_match,
        'expected_body_first': expected_body[0] if expected_body else '',
        'generated_body_first': body_lines[0] if body_lines else '',
        'body_line_ratio': body_line_ratio,
        'capped_body_line_ratio': capped_body_line_ratio,
        'capped_body_coverage': capped_body_coverage,
        'generated_body_lines': body_lines,
        'expected_body_lines': expected_body,
        'capped_expected_body_lines': capped_expected_body,
    }


def main():
    entries = json.loads(JSON_PATH.read_text(encoding='utf-8'))
    app = QApplication([])
    generator = NLPCommitGenerator()
    results = [compare_entry(entry, generator) for entry in entries]

    total = len(results)
    exact_subjects = sum(1 for r in results if r['subject_match'])
    exact_body_counts = sum(1 for r in results if r['body_count_match'])
    capped_body_counts = sum(1 for r in results if r['capped_body_count_match'])
    avg_subject_similarity = sum(r['subject_similarity'] for r in results) / total
    avg_body_ratio = sum(r['body_line_ratio'] for r in results) / total
    avg_capped_body_ratio = sum(r['capped_body_line_ratio'] for r in results) / total
    avg_capped_body_coverage = sum(r['capped_body_coverage'] for r in results) / total

    report = {
        'total_examples': total,
        'max_body_lines': MAX_BODY_LINES,
        'exact_subject_matches': exact_subjects,
        'exact_body_count_matches': exact_body_counts,
        'capped_body_count_matches': capped_body_counts,
        'average_subject_similarity': avg_subject_similarity,
        'average_body_line_ratio': avg_body_ratio,
        'average_capped_body_line_ratio': avg_capped_body_ratio,
        'average_capped_body_coverage': avg_capped_body_coverage,
        'entries': results,
    }

    out_path = ROOT / 'comparison_report.json'
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'Parsed examples: {total}')
    print(f'Exact subject matches: {exact_subjects}')
    print(f'Exact body count matches: {exact_body_counts}')
    print(f'Capped body count matches: {capped_body_counts}')
    print(f'Average subject similarity: {avg_subject_similarity:.3f}')
    print(f'Average body line ratio: {avg_body_ratio:.3f}')
    print(f'Average capped body line ratio: {avg_capped_body_ratio:.3f}')
    print(f'Average capped body coverage: {avg_capped_body_coverage:.3f}')
    print(f'Wrote report to {out_path}')

    print('\nWorst subjects:')
    for r in sorted(results, key=lambda x: x['subject_similarity'])[:10]:
        print(f"- {r['title']}: {r['generated_subject']} vs expected {r['expected_subject']} ({r['subject_similarity']:.2f})")

    print('\nWorst body counts:')
    for r in [r for r in results if not r['body_count_match']][:10]:
        print(f"- {r['title']}: generated {r['generated_body_count']} expected {r['expected_body_count']}")

    print('\nWorst capped body coverage:')
    for r in sorted(results, key=lambda x: x['capped_body_coverage'])[:10]:
        print(f"- {r['title']}: coverage {r['capped_body_coverage']:.2f}")


if __name__ == '__main__':
    main()
