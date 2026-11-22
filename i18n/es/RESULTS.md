<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# Resultados de los agentes de investigación

[English](../../results/README.md) · [中文](../zh/RESULTS.md) · **Español** · [Français](../fr/RESULTS.md) · [Deutsch](../de/RESULTS.md) · [Italiano](../it/RESULTS.md) · [Русский](../ru/RESULTS.md) · [Português](../pt/RESULTS.md) · [العربية](../ar/RESULTS.md)

Esta carpeta la escribe `tools/collect_results.py` a partir de los comentarios públicos de resultados de
[agentes de investigación](../../agent/README.md):

- `REPORT.md`: un resumen legible, con hallazgos verificados y conflictos;
- `summary.json`: lo mismo por tarea, para programas;
- `coverage.json`: cuántos resultados coincidentes tiene cada unidad de cada tarea. Los agentes lo leen para
  preferir las unidades a las que aún les faltan resultados coincidentes; solo es una pista y no necesita firma;
- `ai/`: respuestas de los modelos de IA locales de los participantes, generadas por máquina y sin verificar.

Una unidad se confirma cuando el número de cuentas de GitHub distintas exigido por la tarea
publicó el mismo hash de resultado. Cada «acierto» notificado de la búsqueda de estafa de salida se recalcula
exactamente por el colector antes de que se liste. Qué significan las tareas:
[tasks/README.md](TASKS.md).

Aún no se ha recogido nada de los participantes. Una primera ejecución de la lista completa de tareas en un
ordenador, aún no confirmada por nadie más, se describe en [FIRST_RUN.md](FIRST_RUN.md).
