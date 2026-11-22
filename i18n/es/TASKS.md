<!-- translation of tasks/README.md, source sha256: f0685cfe87baef739cff7ff9121f8ab2fd0aed86866b5638fd79dcdd347c1916 -->

# Tareas para los agentes de investigación

[English](../../tasks/README.md) · [中文](../zh/TASKS.md) · **Español** · [Français](../fr/TASKS.md) · [Deutsch](../de/TASKS.md) · [Italiano](../it/TASKS.md) · [Русский](../ru/TASKS.md) · [Português](../pt/TASKS.md) · [العربية](../ar/TASKS.md)

Esta carpeta contiene el trabajo que toman los [agentes de investigación](../../agent/README.md):

- [`index.json`](../../tasks/index.json): la lista de tareas actual;
- `index.json.sig`: su firma (los agentes ignoran una lista sin una firma válida);
- [`context/`](../../tasks/context): textos congelados que citan las preguntas de IA.

Los resultados aparecen como comentarios en la incidencia de seguimiento de cada tarea y se resumen en
[`results/`](../../results) mediante `tools/collect_results.py`.

## Qué es una tarea

Una tarea son datos: el nombre de un cálculo incorporado en el agente (un «kernel»), sus
parámetros y el número de piezas independientes («porciones») en que se divide el trabajo. Una tarea
no puede llevar código. Un tipo nuevo de cálculo necesita una versión firmada nueva del agente.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

No hay planificador. Cada agente elige una porción aleatoria que no haya hecho. Que varios agentes
caigan en la misma porción es intencionado: todos los cálculos incorporados son aritmética entera exacta, de modo que
el mismo trabajo da las mismas cifras en todos los dispositivos, y una porción cuenta como confirmada cuando
`redundancy` cuentas de GitHub distintas publican la misma huella. Huellas distintas para una porción
son un conflicto que un responsable resuelve recalculándola.

## Cálculos incorporados en el agente 0.1

| Cálculo incorporado | Qué calcula | Fuente |
|---|---|---|
| `selftest@1` | Una carga de trabajo entera fija; todos los dispositivos deben devolver la misma huella | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Pago esperado exacto de un participante que envía resultados falsos y abandona, en una familia de estrategias; informa de las estrategias que superan al abandono honesto | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Probabilidad exacta de un mes o trimestre con pérdidas cuando solo se pagan las tareas comprobadas | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Opcional: una pregunta para un modelo de IA local que ejecuta el participante | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

Cada archivo fuente empieza por el modelo exacto que implementa, de modo que cualquiera puede recalcular un
resultado de forma independiente.

## Las tareas publicadas ahora, y por qué

Todas ellas conciernen a la principal pregunta abierta del proyecto: ¿puede hacerse inútil la trampa
con poco coste? ([OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)).

| Tarea | Pregunta |
|---|---|
| `selftest-1` | ¿Funciona el flujo en su dispositivo? |
| `exit-a-honest-check` | Sin colusión, ¿hay alguna forma de ganar con resultados falsos antes de abandonar? El diseño dice que no |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | Con tareas pequeñas iguales: ¿a partir de qué proporción de verificadores en colusión compensa abandonar con resultados falsos? La estimación del diseño es de aproximadamente un 91% |
| `exit-a-uniform-cap-h399` | Lo mismo con el límite propuesto «como máximo un tercio del importe pendiente en trabajo», en tres oleadas |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | Lo mismo cuando las tareas pueden tener cualquier tamaño, con y sin ese límite |
| `lottery-b-table` | Si solo se pagan las tareas comprobadas, ¿con qué frecuencia tiene un participante pequeño un mes con pérdidas? |
| `ask-variant-b-attack` | Para modelos de IA locales: encuentre un ataque nuevo a «la red paga solo por trabajo comprobado» |

Estos son cálculos sobre las reglas tal y como están escritas en los documentos de diseño. No son
mediciones del hardware ni experimentos con la red. Las tareas de medición (por
ejemplo, si la inferencia entera da los mismos bits en distintas tarjetas gráficas) se
publicarán solo después de que los responsables del proyecto abran los experimentos.

## Proponer una tarea

Abra una incidencia titulada `[Task] …` y diga:

1. la pregunta que responde el cálculo y a qué pregunta abierta pertenece;
2. el modelo exacto, para que pueda recalcularse de forma independiente;
3. qué cálculo incorporado y qué parámetros lo harían, o qué debe calcular un cálculo incorporado nuevo;
4. cómo se detectaría un resultado erróneo o falsificado.

Los responsables comprueban la tarea con `tools/sign_tasks.py --check`, la añaden a `index.json` y firman
la lista. Solo el titular de la clave de publicación puede firmar; véase
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
