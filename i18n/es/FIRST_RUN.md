<!-- translation of results/FIRST_RUN.md, source sha256: 786aa2e462922d0a3a2ec06d0da0e26d246a2563867e215a11cfbf5a799bfe0a -->

# Primera ejecución de la primera lista de tareas (un ordenador, aún sin confirmar)

[English](../../results/FIRST_RUN.md) · [中文](../zh/FIRST_RUN.md) · **Español** · [Français](../fr/FIRST_RUN.md) · [Deutsch](../de/FIRST_RUN.md) · [Italiano](../it/FIRST_RUN.md) · [Русский](../ru/FIRST_RUN.md) · [Português](../pt/FIRST_RUN.md) · [العربية](../ar/FIRST_RUN.md)

El 22 de noviembre de 2026, cada unidad de la lista de tareas número 1 se calculó una vez en un único ordenador con
Windows, con el mismo código que ejecutan los agentes: 702 unidades, 15,5 horas de CPU, sin fallos. Un
ordenador no es una confirmación. Las cifras de abajo se convierten en resultados del proyecto solo cuando
otros participantes publican los mismos hashes (véase [README.md](RESULTS.md)).

## Irse con resultados falsos (núcleo `exit-scam-a@1`, variante A del diseño)

Un participante con un importe H0 «pendiente» presenta resultados falsos en unas pocas tandas rápidas y
se va. Si simplemente se fuera, obtendría H0. La tabla indica la proporción más baja de verificadores en
colusión a partir de la cual alguna estrategia de la familia analizada tiene una ganancia esperada superior a H0.
El modelo exacto está al principio de
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py).

| Tarea | Estrategias analizadas | Rentable a partir de la proporción de colusión | Mejor ganancia esperada en ese punto |
|---|---:|---|---|
| `exit-a-honest-check`: sin colusión, cualquier tamaño de tarea, dos tandas | 92,169,600 | nunca | 0.980 × H0 |
| `exit-a-uniform-h399`: tareas pequeñas iguales, 399 precios pendientes, una tanda | 7,600 | 0.892 (no en 0.890) | 1.0066 × H0 |
| `exit-a-uniform-h1200`: tareas pequeñas iguales, 1200 precios pendientes, una tanda | 22,800 | 0.908 (no en 0.906) | 1.0117 × H0 |
| `exit-a-uniform-cap-h399`: tareas pequeñas iguales, tres tandas, «como máximo un tercio en trabajo» | 71,772,196 | 0.890 (no en 0.888) | 1.0059 × H0 |
| `exit-a-sizes-cap`: cualquier tamaño de tarea, tres tandas, «como máximo un tercio en trabajo» | 1,190,974,992 | 0.875 (no en 0.870) | 1.00004 × H0; 1.034 × H0 en 0.880 |
| `exit-a-sizes-nocap`: cualquier tamaño de tarea, dos tandas, sin ese límite | 69,148,800 | 0.800 (no en 0.780) | 1.218 × H0; 4.91 × H0 en 0.850 |

Qué sugiere:

- La estimación del diseño «hacer trampa da pérdidas mientras quienes coluden tengan menos del 91% aproximadamente» proviene
  del promedio de un único falso. No tiene en cuenta que un participante no puede perder más que
  el importe pendiente (no hay depósitos ni multas). Para quien se va, la pérdida está
  limitada y la ganancia no, lo que reduce el umbral a aproximadamente 87,5–89%.
- La regla propuesta «como máximo un tercio del importe pendiente en trabajo a la vez» es necesaria.
  Sin ella, las recompensas sin verificar de la primera tanda aumentan el importe pendiente y permiten tareas
  mayores en la segunda tanda, y el umbral cae a alrededor del 80%.
- Sin colusión no se encontró ninguna forma rentable de irse con resultados falsos.

Límites: esto es un cálculo en un modelo formal de las reglas, no una medición; la búsqueda
cubre solo las familias indicadas; la rejilla de proporciones de colusión tiene pasos de 0,002 a 0,02.

## Pagar solo por tareas comprobadas (núcleo `lottery-b@1`, variante B del diseño)

Probabilidad de que los ingresos de un periodo estén por debajo del coste del trabajo realizado en él, cuando una
tarea se comprueba con probabilidad 1/P y una tarea comprobada se paga con P precios. Sumas binomiales exactas.

| Tareas al mes | Comprobadas | Coste / precio | Meses con pérdidas | Trimestres con pérdidas |
|---:|---|---:|---:|---:|
| 600 | 1 de cada 10 | 95% | 32.20% | 22.91% |
| 6,000 | 1 de cada 100 | 95% | 33.10% | 24.02% |
| 6,000 | 1 de cada 100 | 80% | 4.84% | |
| 60,000 | 1 de cada 100 | 95% | 10.47% | 1.55% |
| 200,000 | 1 de cada 100 | 95% | 1.15% | |
| 200,000 | 1 de cada 100 | 98% | 18.15% | |
| 600 | 1 de cada 100 | 95% | 44.49% | |

Con 600 tareas al mes y 1 de cada 100 comprobadas, no se paga absolutamente nada en el 0,24% de los meses. La
tabla completa tiene 360 celdas; aparecerá en `summary.json` cuando los agentes la publiquen.
