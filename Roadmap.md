# Roadmap: NLTK + Lightweight ML Git Commit Generator

Este roadmap documenta el progreso del generador de commits inteligente basado en NLTK, extendido con un motor ML clásico y opcional basado en scikit-learn. El objetivo del proyecto es mejorar la predicción de Conventional Commits sin convertirlo en una aplicación pesada de IA: todo debe seguir siendo local, ligero, explicable, mantenible y compatible con Debian 12.

## Contrato del Proyecto

### Filosofía
- [x] Mantener el proyecto ligero, offline-first, open source, Linux friendly y Debian 12 friendly.
- [x] Priorizar estabilidad, compatibilidad offline, compatibilidad Debian, bajo uso de memoria y luego precisión.
- [x] Mantener `smart_commit_nltk.py` funcional como motor heurístico existente.
- [x] Extender la arquitectura actual en vez de reemplazarla.
- [x] Evitar complejidad innecesaria y dependencias pesadas.

### Límites Técnicos
- [x] No usar transformers, torch, tensorflow, spaCy, Hugging Face, redes neuronales, APIs cloud, frameworks LLM, inferencia online ni telemetría.
- [x] Usar dependencias disponibles en repositorios Debian 12: `python3-nltk`, `python3-sklearn`, `python3-joblib`, `python3-langdetect`, `python3-regex`.
- [x] Mantener `python3-gensim` como opcional, no requerido.
- [x] No depender de paquetes pesados instalables solo por pip para la ruta principal.
- [x] Conservar funcionamiento completo sin internet una vez presentes los datos locales de NLTK y, si se usa, el modelo local.

### Responsabilidades por Motor
- [x] NLTK y utilidades locales: normalización, limpieza, tokenización, stemming, stopword removal y preprocessing.
- [x] scikit-learn: vectorización TF-IDF, clasificación ML y predicción del tipo de commit.
- [x] Heurísticas existentes: fallback, generación de subject/body, scope y comportamiento compatible con la UI actual.
- [x] `python3-langdetect`: apoyo para detección de idioma cuando sea útil, con fallback determinista.
- [x] `python3-regex`: mejoras de regex donde aporten valor, con fallback prudente si falta el paquete.

### Objetivo ML
- [x] Predecir tipos Conventional Commit desde texto de usuario.
- [x] Soportar tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.
- [x] Usar `TfidfVectorizer` y `LinearSVC`.
- [x] Guardar modelo local con `joblib`.
- [x] Guardar vectorizer separado.
- [x] Cargar rápido y fallar sin romper la aplicación.
- [x] No usar inferencia online ni servicios externos.

## Estado Actual para Retomar

El programa ya es funcional para uso diario: toma texto pegado en español o inglés, limpia ruido de Markdown/comandos, detecta idioma, propone `type(scope)`, genera subject y body localizado, permite corregir manualmente idioma/type/scope y copia el comando sin ventana modal.

La línea de mejora actual no es integrar con Git, sino mejorar la calidad semántica desde el texto pegado. La mejora ML debe permanecer como una capa opcional, clásica y local encima del motor NLTK, no como reemplazo.

### Últimos Avances Importantes
- [x] Eliminada la vista previa separada de subject/body porque no aportaba al flujo.
- [x] Añadido truncado inteligente de subject con límites de palabra.
- [x] Corregida la priorización para que cambios semánticos no queden ocultos por menciones secundarias de tests o documentación.
- [x] Añadida detección general de validaciones indirectas como `Resultado: 20 tests OK`, `suite completa pasa`, `py_compile`, `compileall`, `unittest` y `pytest`.
- [x] Añadida detección de menciones de archivos para clasificar código, tests, documentación, reportes y configuración.
- [x] Ampliado el body de 5 a 7 bullets para conservar detalles importantes.
- [x] Añadido ranking de bullets para poner primero cambios principales, luego tests/docs/reportes y dejar validación al final.
- [x] Añadida arquitectura ML opcional con scikit-learn, TF-IDF, LinearSVC y fallback a heurísticas NLTK.
- [x] Suite actual: 26 tests registrados: 25 pasan y 1 entrenamiento se omite si `python3-sklearn` no está instalado.

### Estado de Cumplimiento del Prompt ML
- [x] `smart_commit_nltk.py` permanece y sigue siendo funcional.
- [x] El motor sklearn es modular y opcional.
- [x] La aplicación funciona aunque falten `ml/commit_model.pkl` y `ml/vectorizer.pkl`.
- [x] El entrenamiento reutiliza `commit_examples_data/examples.json`, `commit_examples_data/examples.db` y `commit_examples_data/entries/`.
- [x] El predictor devuelve tipo y confianza aproximada cuando el modelo lo permite.
- [x] El sistema soporta entrada en inglés y español.
- [x] El proyecto incluye `ml/`, `utils/` y tests dedicados para la nueva arquitectura.
- [x] Los artefactos `ml/*.pkl` se tratan como generados localmente y no se versionan por defecto.
- [ ] Validar entrenamiento real y predicciones con `python3-sklearn` instalado en Debian 12.
- [ ] Se distribuirá un modelo preentrenado, y si el usuario lo desea tendrá las instrucciones para que lo entrene localmente según el lo necesite

### Ejemplo de Calidad Actual

Entrada resumida:

```text
Mejoré la detección de menciones de archivos dentro del texto pegado.
Actualicé smart_commit_nltk.py, tests/test_smart_commit_nltk.py, README.md,
Roadmap.md y commit_examples_data/comparison_report.json.
Resultado: 19 tests OK.
```

Salida esperada actual:

```bash
git commit -m "feat(nlp): mejora detección de menciones de archivos" \
  -m "- Actualiza lógica de código mencionada en el resumen" \
  -m "- Cubre cambios con tests de regresión" \
  -m "- Actualiza documentación mencionada en el resumen" \
  -m "- Actualiza datos o reportes de evaluación" \
  -m "- Validación: 19 tests pass"
```

### Comandos Útiles

Instalar dependencias Debian:

```bash
sudo apt install \
    python3-pyqt6 \
    python3-nltk \
    python3-sklearn \
    python3-joblib \
    python3-langdetect \
    python3-regex
```

Dependencia opcional:

```bash
sudo apt install python3-gensim
```

Entrenar o reentrenar el modelo ML local:

```bash
python3 -m ml.train_model
```

Ejecutar la suite de regresión:

```bash
QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -v
```

Recalcular el reporte de comparación:

```bash
QT_QPA_PLATFORM=offscreen python3 commit_examples_data/compare_generator.py
```

Nota: `__pycache__/smart_commit_nltk.cpython-311.pyc` puede aparecer modificado porque ya está trackeado por Git. `.gitignore` evita nuevos artefactos, pero queda pendiente sacarlo del índice.

## Funcionalidades Completadas

### [x] Configuración Inicial del Proyecto
- [x] Creación del repositorio y estructura básica.
- [x] Instalación de dependencias principales: NLTK y PyQt6.
- [x] Verificación inicial de datos NLTK requeridos al arrancar la aplicación.
- [x] Descarga automática de paquetes NLTK faltantes en el primer uso.
- [x] Documentación de paquetes Debian requeridos para el motor ML opcional.
- [x] Documentación de `python3-gensim` como dependencia opcional.

### [x] Interfaz de Escritorio
- [x] Ventana principal en PyQt6 para pegar resúmenes de cambios.
- [x] Botón para generar commits con NLTK.
- [x] Botón para limpiar el texto de entrada del usuario.
- [x] Indicador de idioma detectado: pendiente, Español o Inglés.
- [x] Selector manual de idioma: Automático, Español o Inglés.
- [x] Selectores manuales para ajustar type y scope antes de copiar.
- [x] Advertencia no intrusiva cuando el input tiene mucho ruido o bloques de código.
- [x] Área de salida con comando `git commit` multilinea.
- [x] Botón para copiar el comando al portapapeles.
- [x] Confirmación de copiado en el propio botón, sin mensaje modal.

### [x] Generador Base con NLTK
- [x] Tokenización y POS tagging para textos en inglés.
- [x] Extracción inicial de verbo y objeto para construir el subject.
- [x] Scoring de oraciones para elegir la frase más representativa.
- [x] Formato Conventional Commits: `type(scope): subject`.
- [x] Límite de longitud para subject y body lines.

### [x] Dataset de Ejemplos de Commits
- [x] Creación de `COMMIT_GENERATION_EXAMPLES.md` con casos reales.
- [x] Desarrollo de `parse_commit_examples.py` para parsear ejemplos.
- [x] Exportación de ejemplos a JSON y SQLite.
- [x] Validación de 45 entradas procesadas correctamente.

### [x] Sistema de Comparación y Evaluación
- [x] Creación de `compare_generator.py`.
- [x] Comparación entre commits generados y commits esperados.
- [x] Reporte JSON con métricas de similitud.
- [x] Mejora inicial de similitud de 0.453 a 0.528.
- [x] Aumento posterior de similitud del subject a 0.509.
- [x] Actualización de `compare_generator.py` para la firma bilingüe actual.
- [x] Recalculo de `comparison_report.json` tras las mejoras bilingües.
- [x] Registro de línea base actual: 45 ejemplos, subject similarity 0.446, body ratio 0.000.

### [x] Filtrado de Ruido
- [x] Eliminación de comandos de terminal y frases conversacionales irrelevantes.
- [x] Limpieza de líneas generadas por herramientas o asistentes.
- [x] Filtrado de bloques Markdown con triple backtick.
- [x] Ignorar comandos `git commit -m` pegados dentro del resumen.
- [x] Ignorar líneas `-m` incrustadas para evitar que contaminen el body.
- [x] Limpieza de enlaces Markdown, conservando el texto visible del enlace.
- [x] Conservación de validaciones útiles como `py_compile` cuando aparecen dentro de bloques de código.

### [x] Soporte Bilingüe Español/Inglés
- [x] Detección simple de idioma de entrada (`es` / `en`).
- [x] Tokenización por idioma usando Punkt en inglés o español.
- [x] Generación del subject y body en el mismo idioma del resumen.
- [x] Soporte para verbos españoles comunes: `creado`, `actualizado`, `incluye`, `resume`, `corrige`, `mejora`.
- [x] Extracción de objetos en español mediante reglas lingüísticas propias.
- [x] Casos específicos para resúmenes de roadmap en español e inglés.
- [x] Casos específicos para mejoras bilingües/NLP.

### [x] Detección de Type y Scope
- [x] Detección automática de tipos: `feat`, `fix`, `docs`, `test`, `build`, `ci`, `style`, `refactor`, `perf`.
- [x] Detección automática de scopes: `app`, `ui`, `docs`, `repo`, `dict`, `tools`, `nlp`.
- [x] Corrección del falso positivo de `ci` dentro de palabras como `funcionalidades` o `secciones`.
- [x] Priorización de cambios NLP/bilingües como `feat(nlp)`.
- [x] Clasificación de roadmaps creados como `docs(repo)`.

### [x] Motor ML Ligero y Opcional
- [x] Creación de `ml/dataset_loader.py` para reutilizar `examples.json`, `examples.db` y `commit_examples_data/entries/`.
- [x] Creación de `ml/train_model.py` con `TfidfVectorizer` y `LinearSVC`.
- [x] Guardado local de `commit_model.pkl` y `vectorizer.pkl` mediante `joblib`.
- [x] Creación de `ml/predictor.py` con carga rápida y fallo silencioso hacia heurísticas.
- [x] Semillas offline para cubrir `feat`, `fix`, `docs`, `refactor`, `test` y `chore`.
- [x] Utilidades compartidas en `utils/` para preprocessing NLTK, detección de idioma y `python3-regex`.
- [x] Documentación de instalación Debian, entrenamiento local y comportamiento sin modelo.
- [x] Separación inicial entre responsabilidades NLTK/preprocessing y sklearn/clasificación.
- [x] Fallback automático al motor heurístico cuando falla la predicción ML.

### [x] Arquitectura Offline y Extensible
- [x] Mantener motor heurístico existente como fallback.
- [x] Añadir motor sklearn sin romper el flujo de UI actual.
- [x] Preparar estructura para futuros motores: heurístico, sklearn y posible motor futuro opcional.
- [x] Evitar cualquier dependencia de red, API externa, telemetría o inferencia online.
- [x] Mantener artefactos de modelo como archivos locales generados por `joblib`.

### [x] Generación de Body Lines
- [x] Generación de hasta 7 bullets relevantes.
- [x] Bullets localizados en español o inglés según el texto de entrada.
- [x] Bullets específicos para roadmap con seguimiento de progreso.
- [x] Bullets específicos para soporte bilingüe/NLP.
- [x] Bullets de validación para `compileall`, pruebas y `py_compile`.
- [x] Dedupe básico para evitar bullets repetidos.

### [x] Documentación
- [x] README actualizado con capacidades actuales.
- [x] Ejemplos de salida en español e inglés.
- [x] Roadmap actualizado con funcionalidades completadas y pendientes.
- [x] README actualizado con comandos de testing y evaluación.

### [x] Evaluación y Testing Inicial
- [x] Creación de suite `unittest` para regresiones principales.
- [x] Tests para `strip_markdown_noise()`.
- [x] Tests para detección de idioma.
- [x] Tests para generación bilingüe `feat(nlp)` en español e inglés.
- [x] Test para roadmap en español como `docs(repo)`.
- [x] Test para evitar falso positivo de `ci` dentro de palabras comunes.
- [x] Test para priorizar summaries de testing/evaluación sobre términos bilingües.
- [x] Test para limpiar entrada, salida y estado del botón copiar.
- [x] Test para priorizar summaries del botón Limpiar entrada sobre menciones de tests/Roadmap.
- [x] Test para mostrar y reiniciar el idioma detectado en la interfaz.
- [x] Test para priorizar summaries de idioma detectado sobre menciones de Roadmap.
- [x] Test para forzar manualmente el idioma de generación.
- [x] Test para editar manualmente type/scope y regenerar el comando.
- [x] Test para priorizar summaries de type/scope sobre menciones de tests/Roadmap.
- [x] Test para confirmar copiado en el botón sin mensaje modal.
- [x] Test para advertencias de ruido por bloques de código y commits pegados.
- [x] Test para truncar el subject sin cortar palabras.
- [x] Test para priorizar summaries de eliminación de vista previa y truncado sobre menciones de tests.
- [x] Test para detectar validaciones indirectas como `suite completa pasa: 18 tests OK`.
- [x] Test para detectar menciones de código, tests, documentación y reportes.
- [x] Test para ordenar bullets por importancia y podar documentación genérica duplicada.
- [x] Tests para dataset loader y fallback del predictor ML cuando no hay modelo.
- [x] Tests unitarios para extracción de acciones comunes en español.
- [x] Tests directos para `select_commit_type()` con categorías core.
- [x] Tests directos para `detect_scope()` con áreas comunes del proyecto.
- [x] Ejecución exitosa de la suite: 25 tests pasan y 1 se omite sin `python3-sklearn`.

### [x] Higiene de Artefactos Generados
- [x] Creación de `.gitignore` para `__pycache__/` y archivos `*.py[cod]`.

## Mejoras Futuras Pendientes

### Siguiente Sesión Recomendada
- [ ] Probar el programa con el texto del último resumen generado por Codex y comparar contra el commit que daría una IA.
- [ ] Si el subject sale demasiado genérico, añadir una regla específica de subject antes de tocar el body.
- [ ] Si el body sale con bullets buenos pero mal ordenados, ajustar `rank_body_lines()`.
- [ ] Si se pierde información útil del texto pegado, revisar primero `clean_input()`.
- [ ] Después de cada mejora, añadir o ajustar un test de regresión en `tests/test_smart_commit_nltk.py`.
- [ ] Ejecutar siempre `QT_QPA_PLATFORM=offscreen python3 -m unittest discover -s tests -v`.

### [ ] Evaluación y Testing
- [x] Añadir más tests unitarios para extracción de acciones en español.
- [x] Añadir más tests unitarios para `select_commit_type()` y `detect_scope()`.
- [ ] Añadir tests de predicción ML con un modelo entrenado cuando `python3-sklearn` esté disponible.
- [ ] Probar en Debian 12 con `python3-sklearn`, `python3-joblib`, `python3-langdetect` y `python3-regex` instalados desde apt.
- [ ] Verificar ejemplos prompt: crash/audio -> `fix`, MIDI karaoke -> `feat`, instrucciones -> `docs`, código deprecated -> `refactor`.
- [ ] Añadir casos de regresión para textos mixtos español/inglés.
- [ ] Añadir casos de regresión para resúmenes con varios archivos modificados.
- [ ] Definir nuevas métricas que no penalicen el límite actual de 7 bullets.
- [ ] Mejorar métricas del dataset histórico sin perder los casos bilingües recientes.

### [ ] Motor ML y Datos
- [ ] Evaluar balance del dataset: actualmente los ejemplos históricos favorecen `feat`.
- [ ] Añadir más ejemplos reales para `fix`, `docs`, `refactor`, `test` y `chore`.
- [ ] Medir precisión del modelo entrenado localmente sin aumentar peso ni complejidad.
- [ ] Documentar criterio para regenerar `commit_model.pkl` y `vectorizer.pkl`.
- [ ] Mantener semillas offline solo como apoyo mientras el dataset real crece.

### [ ] Soporte Lingüístico
- [ ] Ampliar verbos y patrones en español.
- [ ] Mejorar detección de idioma para textos mixtos.
- [ ] Separar reglas por idioma en estructuras más mantenibles.
- [ ] Evaluar un etiquetador POS en español si se desea más precisión gramatical.
- [ ] Soportar variantes regionales y frases más coloquiales.

### [ ] Arquitectura y Mantenibilidad
- [x] Añadir módulos externos para preprocessing, idioma y motor ML sin reescribir `smart_commit_nltk.py`.
- [ ] Separar completamente la lógica NLP heurística de la interfaz PyQt6.
- [ ] Crear una clase o módulo dedicado para limpieza de input.
- [ ] Crear un módulo dedicado para type/scope detection.
- [ ] Crear fixtures reutilizables con ejemplos reales.
- [ ] Decidir si los artefactos `ml/*.pkl` deben distribuirse preentrenados o mantenerse como generación local.
- [ ] Definir una interfaz común de motores para `heuristic`, `sklearn` y futuros motores opcionales.
- [ ] Sacar del índice de Git cualquier `__pycache__` ya trackeado.

### [ ] Interfaz de Usuario
- [x] Permitir cambiar manualmente el idioma detectado.
- [x] Permitir editar type/scope desde la UI antes de copiar.
- [x] Mostrar advertencias cuando el input tenga mucho ruido o muchos bloques de código.

### [ ] Calidad del Commit
- [x] Mejorar ranking de bullets por importancia.
- [x] Detectar validaciones y pruebas aunque aparezcan en frases indirectas.
- [x] Detectar menciones de documentación, tests y código dentro del texto pegado.
- [x] Mejorar truncado de subject para que no corte palabras.
- [x] Ampliar el body hasta 7 bullets para conservar cambios relevantes y validación.
- [x] Priorizar mejoras semánticas combinadas sobre menciones secundarias de tests/documentación.
- [ ] Generar alternativas cuando haya varias interpretaciones posibles.

---

**Última actualización:** 12 de mayo de 2026  
**Estado:** Funcional para uso básico e iteración diaria; ya cuenta con regresiones iniciales, evaluación del dataset y motor ML opcional offline. La prioridad siguiente es mejorar la calidad semántica desde el texto pegado sin perder ligereza ni compatibilidad Debian.
