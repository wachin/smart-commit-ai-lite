"""Input cleanup helpers for pasted commit summaries."""

from __future__ import annotations

from utils.regex_utils import regex as re


ACTION_PATTERN = re.compile(
    r'\b(we|i|added|created|implemented|updated|changed|fixed|fixes|refactored|cleaned|improved|made|'
    r'detects|detect|uses|use|loads|load|writes|write|reports|report|normalizes|normalize|covers|cover|documents|document|'
    r'supports|support|generates|generate|validated|validate|'
    r'he|hemos|creado|creé|creamos|añadido|añadí|añadimos|agregado|implementado|implementé|implemente|actualizado|'
    r'actualicé|actualice|actualizamos|recalculé|recalcule|afiné|afine|cambiado|corregido|'
    r'arreglado|arreglé|arreglamos|arregló|mejorado|mejoré|mejore|mejoramos|documenta|documentado|documentada|documentamos|incluye|resume|'
    r'detecta|usa|entiende|genera|corrige|corregí|corregi|verifiqué|verifique|validé|valide|'
    r'le metí|metí|le puse|puse|puedes|selectores|tipo|scope|regenera|manteniendo|ajuste|manual|'
    r'añadí|anadi|quité|quite|quitada|eliminé|elimine|elimina|borra|borrar|desactiva|devuelve|foco|resultado|tests|'
    r'continué|continue|trunca|truncado|truncate_subject|vista previa|límites de palabra|limites de palabra|'
    r'limpiado|ajustado|clarify|clearer|explicit|supported|local|debian|contribution|guidance|'
    r'joblib|principles|constraints|labels|responsibility split|do not use|'
    r'idioma detectado|pendiente|español|inglés|integración|integracion|baseline|línea base|linea base|quedó|quedo)\b',
    re.IGNORECASE,
)


def clean_summary_text(text: str) -> str:
    text = re.sub(r'\[.*?\]', ' ', text)
    text = text.replace('..', '.')
    return re.sub(r'\s+', ' ', text).strip()


def strip_markdown_noise(text: str) -> str:
    cleaned_lines = []
    in_fence = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            if 'py_compile' in line:
                cleaned_lines.append(f"Verifiqué con {line}.")
            continue
        if re.search(r'^\s*git\s+commit\b', line):
            continue
        if re.search(r'^\s*-m\s+["\']', line):
            continue
        cleaned_lines.append(raw_line)

    text = '\n'.join(cleaned_lines)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def clean_input(text: str) -> str:
    text = strip_markdown_noise(text)
    cleaned_lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if re.search(r'^(Read|Ran terminal command|Replacing|Made changes|Replacing \d+ lines)', line, re.IGNORECASE):
            continue
        if re.search(r'^(command -v|for f in|echo|----|sed|pdftotext|python3)', line):
            continue
        if re.search(r'^(file:///|lines \d+ to \d+|content\.txt)', line):
            continue
        if re.search(r'^(Replacing \d+ lines with \d+ lines)', line):
            continue
        if re.search(r'^(Voy a|Reviso la|Encuentro que|He encontrado|Verifico si)', line):
            continue
        if re.search(r'^(Y analizo|Sed|Replacing)', line):
            continue
        if len(line) < 10 or not ACTION_PATTERN.search(line):
            continue
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def detect_input_noise_warnings(text: str) -> list[str]:
    warnings = []
    fenced_blocks = len(re.findall(r'```', text)) // 2
    embedded_commits = len(re.findall(r'^\s*git\s+commit\b', text, re.MULTILINE))
    message_parts = len(re.findall(r'^\s*-m\s+["\']', text, re.MULTILINE))
    original_lines = [line for line in text.splitlines() if line.strip()]
    cleaned_lines = [line for line in clean_input(text).splitlines() if line.strip()]

    if fenced_blocks:
        warnings.append(f"{fenced_blocks} bloque(s) de código")
    if embedded_commits or message_parts:
        warnings.append("commits pegados")
    if original_lines and len(cleaned_lines) <= max(1, len(original_lines) // 3):
        warnings.append("mucho ruido filtrado")

    return warnings
