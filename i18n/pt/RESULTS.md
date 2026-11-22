<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# Resultados dos agentes de pesquisa

[English](../../results/README.md) · [中文](../zh/RESULTS.md) · [Español](../es/RESULTS.md) · [Français](../fr/RESULTS.md) · [Deutsch](../de/RESULTS.md) · [Italiano](../it/RESULTS.md) · [Русский](../ru/RESULTS.md) · **Português** · [العربية](../ar/RESULTS.md)

Esta pasta é escrita por `tools/collect_results.py` a partir dos comentários públicos de resultados dos
[agentes de pesquisa](../../agent/README.md):

- `REPORT.md`: um resumo legível, incluindo descobertas verificadas e conflitos;
- `summary.json`: o mesmo por tarefa, para programas;
- `coverage.json`: quantos resultados concordantes cada unidade de cada tarefa tem. Os agentes o leem para
  preferir unidades que ainda não têm resultados; é apenas uma dica e não precisa de assinatura;
- `ai/`: respostas dos modelos locais de IA dos participantes, geradas por máquina e não verificadas.

Uma unidade é confirmada quando o número de contas diferentes do GitHub exigido pela tarefa
publicou o mesmo hash de resultado. Cada "acerto" relatado da busca de golpe de saída é recalculado
exatamente pelo coletor antes de ser listado. O que as tarefas significam:
[tasks/README.md](TASKS.md).

Nada foi coletado dos participantes ainda. Uma primeira execução da lista completa de tarefas em um
computador, ainda não confirmada por mais ninguém, é descrita em [FIRST_RUN.md](FIRST_RUN.md).
