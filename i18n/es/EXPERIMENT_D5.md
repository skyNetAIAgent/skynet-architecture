<!-- translation of docs/EXPERIMENT_D5.md, source sha256: a043f1ab15bdb60165b5430029b58928dbd99d6807c243175827dd51c9421af4 -->

# Experimento D5: Qwen3.5-4B entero

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · **Español** · [Français](../fr/EXPERIMENT_D5.md) · [Deutsch](../de/EXPERIMENT_D5.md) · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · [Português](../pt/EXPERIMENT_D5.md) · [العربية](../ar/EXPERIMENT_D5.md)

Estado a 25 de noviembre de 2026: **los bits coinciden en seis ejecutores, incluido el contexto largo;
O3 y O4 están medidos y no cumplieron los umbrales; la calidad (O5) aún no se ha medido** (sección 7). El experimento está autorizado por la decisión D5
([ROADMAP](ROADMAP.md), sección 3) y forma parte de la etapa 5 de la hoja de ruta. Comprueba el principal supuesto no medido
del mejor candidato de la etapa 4 — la verificación de la respuesta por el propio pagador (PPS,
[VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), secciones 3.2 y 5.2).

## 1. Qué se comprueba

El pagador que tiene el modelo debe recalcular en una sola pasada la petición y la respuesta recibida
y obtener **los mismos bits** que el ejecutor al generar. Esto es posible solo si toda
la aritmética del modelo está definida con números enteros con redondeo fijado: la suma de enteros no depende
del orden de la suma mientras no haya desbordamiento. El experimento responde a cinco preguntas; los criterios
de refutación se fijan antes del lanzamiento:

| Experimento | Pregunta | Qué lo refuta |
|---|---|---|
| O1 | ¿Coinciden los bits en tarjetas gráficas distintas y en el procesador | Al menos un bit distinto de los logits, del token elegido, de la causa de parada o de los hashes de control con la misma entrada. Antes de la conclusión — búsqueda de la primera discrepancia y repetición con la entrada más corta. La conclusión se refiere solo a los dispositivos probados y a la versión de la implementación |
| O2 | ¿Coinciden los bits al generar token a token y en una sola pasada sobre la secuencia completa en una misma tarjeta | Cualquier bit distinto, incluido el hash del estado recurrente de las capas Gated DeltaNet en los puntos de control |
| O3 | ¿Cuánto cuesta la verificación de la respuesta en comparación con su generación | La mediana de la proporción `ρ(1)` mayor que 5% al menos para uno de los cuatro pares de longitudes de petición y respuesta nombrados de antemano con lote 1. Los lotes 8 y 32 se miden por separado |
| O4 | ¿Cuánto más lento es el perfil entero que el habitual de 8 bits en la misma tarjeta | La mediana de la ralentización mayor que 1,25 veces en la celda comparable (el umbral es diagnóstico: deciden O3 y O5) |
| O5 | ¿Cuánta calidad se pierde | La pérdida de precisión mayor que 3 puntos porcentuales en 320 tareas elegidas de antemano (64 de cada uno de los cuatro apartados de MMLU y del MGSM ruso) en comparación con el perfil habitual de 8 bits del mismo modelo |

El 1,2–3,8% calculado de la etapa 4 no se considera resultado de O3: solo este experimento lo confirma
o lo refuta.

## 2. Modelo y equipo

- **Modelo:** repositorio oficial Qwen/Qwen3.5-4B en Hugging Face, revisión fijada
  `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Dos archivos de pesos de 5 329 398 688 y 3 990 429 408
  bytes, en total unos 9,3 GB. Tras la descarga se cotejan los SHA-256 del inventario del repositorio.
- **Arquitectura** (según el `config.json` publicado): 32 bloques, vector oculto 2560, MLP 9216.
  Cada cuarto bloque (índices 3, 7, …, 31) es atención completa: 16 cabezas de consulta, 4 cabezas
  de clave y valor, tamaño de cabeza 256, puerta de salida, rotación de las primeras 64 coordenadas. Los otros
  24 bloques son Gated DeltaNet: estado recurrente 32 × 128 × 128 por bloque, convolución causal
  de profundidad 4. Vocabulario 248 320, matrices de entrada y salida compartidas. El «INT-canónico»
  de transformador habitual de la etapa 4 no le basta; el perfil se define de nuevo (sección 3).
- **Dispositivos:** RTX 2060 6 GB (Turing) en el Linux doméstico del acompañante; RTX 4070 Laptop
  8 GB (Ada) en el ordenador del propietario; el procesador como tercer ejecutor independiente. Con su consentimiento —
  dispositivos de otros participantes mediante un miniagente.
- **Memoria** [cálculo]: los pesos principales de 8 bits — 4010 MiB. Con lote 1 y longitud de hasta 3000 tokens
  todo cabe en 6 GB; el lote 32 con longitud 3000 requiere unos 7064 MiB aun antes de los búferes de trabajo
  y en la RTX 2060 solo es posible con traslado de la historia a la memoria RAM.

## 3. Perfil entero

El perfil recibe un nombre y una versión aparte y se congela antes de O1–O5. La base es el grafo numérico
del proyecto de ChatGPT con las correcciones de ambos críticos:

1. **Pesos y activaciones.** Pesos de 8 bits por filas, escala de la fila — número binario exacto.
   Activaciones de 16 bits con coma fija (1024 = unidad). El redondeo es el mismo para todas
   las operaciones: al más cercano, la mitad — al par, por módulo y con devolución del signo.
2. **Normalizaciones y no linealidades** (RMSNorm, L2, SiLU, sigmoide, softplus, exponencial) — fórmulas
   enteras con raíz cuadrada entera y tablas. Las tablas se construyen fuera del programa con redondeo correcto
   demostrado (MPFR) y se publican con SHA-256.
3. **Atención completa.** Puntuaciones, exponencial por tabla, proporciones en 16 bits. El crítico ChatGPT encontró
   en el proyecto original un error: con valores iguales, añadir otra clave igual
   cambiaba la salida de 1365 a 683. Corrección: dividir la suma ponderada entre la suma de las propias proporciones
   redondeadas; entonces el valor constante se conserva exactamente.
4. **Gated DeltaNet.** Decaimiento, corrección y actualización del estado — cinco asignaciones enteras
   por cada token en un único orden canónico por tiempo. La fórmula del proyecto de DeepSeek
   describía otra recursión y se rechazó. La forma «por bloques» acelerada solo se admite
   si reproduce los mismos bits en cada token.
5. **Elección del token.** Máximo por el par (puntuación, −número) en todo el vocabulario, de forma codiciosa. Un modo aparte —
   Gumbel-max canónico con pseudoaleatoriedad HMAC-SHA256 a partir de la semilla de la petición (D22).
   La parada — primera causa: EOS o límite.
6. **Límites de desbordamiento** definidos para cada acumulador; donde 32 bits no bastan, se usan 64.
   Pruebas aparte comprueban los valores extremos.

Todos los lugares ambiguos («bifurcaciones») se cierran antes del primer lanzamiento leyendo el código fuente del modelo
de la versión fijada de Transformers; el hash de ese código fuente entra en el manifiesto del perfil.

## 4. Orden de los trabajos

1. **P0, preparación (2–4 días).** Descarga y cotejo del modelo; inventario de todos los tensores; cierre de las
   bifurcaciones según el código fuente; tablas; vectores de control con valores manuales.
2. **Paso recortado (1–1,5 semanas).** Referencia en el procesador para todo el modelo con entradas cortas;
   cotejo con el cálculo habitual en coma flotante (solo para detectar un error de importación,
   no para O1/O2). Versión simple para tarjeta gráfica sin núcleos tensoriales. Respuestas de O2 en una tarjeta
   y de O1 «procesador frente a RTX 2060» con contexto corto. Después, el mismo lote en la RTX 4070
   Laptop — primera respuesta de O1 para dos tarjetas gráficas distintas.
3. **Paso completo (3–4 semanas).** Multiplicaciones rápidas de 8 bits, kernel fusionado de la recursión DeltaNet,
   lotes 1/8/32, experimentos O3, O4, O5, repetición en el segundo dispositivo.

Todo el trabajo se realiza en un directorio aparte en el Linux doméstico, con un entorno Python
propio (CuPy con las bibliotecas CUDA 12 de los paquetes pip, sin instalación del sistema). Los servicios activos
y los directorios de otros experimentos no se tocan. La estimación total — 4–6 semanas de trabajo de un
desarrollador; los riesgos principales — el precio de la recursión DeltaNet (lo mostrará O3), las ambigüedades
hasta P0 y el soporte de Qwen3.5 en los motores habituales para O4/O5.

## 5. Qué se publicará

Para cada ejecución: manifiesto del perfil y de las versiones, entradas, hashes de logits y de estados por capas,
tiempos brutos y condiciones de medición, fallos originales junto con sus correcciones. La coincidencia de bits
se refiere solo a los dispositivos y versiones probados. El resultado de cada experimento se anota en la hoja de ruta
(etapa 5) y en este documento; el experimento se considera terminado cuando lo ha repetido un segundo participante.

## 6. Quién hizo qué

- **Proyectos del experimento:** dos proyectos independientes — ChatGPT y DeepSeek.
- **Crítica cruzada:** ChatGPT analizó ambos proyectos, DeepSeek analizó ambos proyectos;
  recálculos de memoria y de límites, comprobación de la recursión corta y de la corrección de la atención con pequeñas búsquedas exhaustivas.
- **Consolidación y decisiones sobre el plan:** Claude.
- **Preparación, perfiles v1 y v2, referencia en el procesador y versión para tarjeta gráfica:** ChatGPT.
- **Comprobaciones independientes:** DeepSeek — importación del modelo con el forward oficial, univocidad
  y límites de desbordamiento del perfil v2.
- **Ejecuciones en las tarjetas gráficas y comprobación de los resultados:** Claude (la tarjeta gráfica
  no está disponible desde la zona de pruebas de modelos).

## 7. Resultados

**24 de noviembre de 2026, entradas cortas.** Entradas: dos historias de 8 + 8 tokens y seis textos cortos
(ruso, inglés, chino, aritmética, código, receta), profundidad 4 y 32 bloques; lote 1.

- **Importación del modelo.** El cálculo habitual en coma flotante, escrito según el código fuente, coincidió
  con el forward oficial de Transformers 5.24.0: el mismo token elegido en 130 de 130 posiciones,
  una desviación de los logits no mayor que 3,6·10⁻⁵ (lo comprobaron ChatGPT y, de forma independiente, DeepSeek).
- **Perfil v1 rechazado.** Se reproducía bit a bit, pero la escala 1/1024 era demasiado gruesa:
  la salida de la recursión DeltaNet se redondeaba casi por completo a cero, la coincidencia del token elegido
  con el modelo fue de 5 de 8, correlación de los logits alrededor de 0,8.
- **Perfil v2** (activaciones con exponente binario por vector y mantisa de 16 bits, resto
  y estado de la recursión con paso 2⁻²⁰, claves y valores de atención en 32 bits): el mismo token que
  el modelo oficial en 90 de 90 posiciones, correlación media de los logits 0,9996, mínima
  0,998. El estado y la caché ocupan 238 MiB con 3000 posiciones frente a 95 de v1; el número de multiplicaciones
  por token es el mismo: 4,2 mil millones.
- **O2 (un dispositivo).** La generación token a token y la pasada sobre la respuesta ya generada, dividida
  en 1, 3 y 8 posiciones, dan los mismos bits de todos los logits, de los tokens elegidos y de los hashes de estados.
- **O1 (dispositivos distintos).** Procesador (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) y RTX 4070
  Laptop (Ada, Windows, CuPy): 88 comparaciones en cada tarjeta, 242 360 320 logits por tarjeta,
  976 tokens elegidos y 37 152 hashes de estados — **ni una sola diferencia**.

**25 de noviembre de 2026, otra arquitectura y otro lenguaje de kernels.** Tercera implementación en OpenCL
(ChatGPT), las mismas entradas y 88 comparaciones: el procesador mediante pocl, la RTX 2060 mediante NVIDIA OpenCL
y la **AMD Radeon RX 580** (Polaris, Mesa rusticl, Linux) — de nuevo ni una sola diferencia en ninguno de los
242 360 320 logits, 976 tokens y 37 152 hashes. En total, los mismos bits en seis ejecutores:
procesador (NumPy), procesador (pocl), RTX 2060 (CUDA y OpenCL), RTX 4070 Laptop (CUDA),
RX 580 (OpenCL).

**25 de noviembre de 2026, contexto largo.** Petición + respuesta: 512 + 64, 2048 + 256 y 4096 + 64 tokens
(textos reales), los 32 bloques; se compararon los hashes de los logits de cada posición, los tokens elegidos
y los hashes de estados cada 64 posiciones. La RTX 2060 (CUDA), la RTX 2060 (OpenCL) y la RTX 4070 Laptop
(CUDA) coincidieron entre sí en los tres casos, y en cada tarjeta la generación token a token coincidió
con la pasada sobre la respuesta ya generada en fragmentos de 64 y 512 posiciones. Para 512 + 64, lo mismo
dieron la referencia independiente en el procesador y la RX 580. En la RX 580 la generación token a token
coincidió con las demás tarjetas también para 2048 + 256 y 4096 + 64, pero la pasada sobre la respuesta ya
generada con entradas largas se interrumpe por el controlador (reinicio de una tarea de la tarjeta
gráfica demasiado larga); hay que dividir el núcleo de atención en partes. Es una limitación de ejecución,
no una discrepancia de bits.

**25 de noviembre de 2026, núcleos rápidos, O3 y O4.** ChatGPT escribió núcleos rápidos para NVIDIA
(DP4A para las multiplicaciones de pesos de 8 bits por activaciones de 16 bits, multiplicaciones por bloques para la pasada
sobre la respuesta, recursión DeltaNet fusionada). En la RTX 2060 y la RTX 4070 Laptop, cada una de las cuatro etapas
de aceleración dio los mismos bits: 88 de 88 comparaciones cortas y el caso largo 512 + 64 frente a la referencia
en el procesador.

O3 — tiempo de verificación de la respuesta en una sola pasada como proporción del tiempo de generación, mediana de nueve pares
tras dos calentamientos:

| Petición / respuesta | RTX 2060, lote 1 | RTX 4070 Laptop, lote 1 | RTX 2060, lote 8 | RTX 4070 Laptop, lote 8 |
|---|---:|---:|---:|---:|
| 128 / 32 | 0,40 | 0,24 | 0,64 | 0,46 |
| 128 / 128 | 0,21 | 0,11 | 0,42 | 0,26 |
| 500 / 500 | 0,21 | 0,10 | 0,43 | 0,28 |
| 2000 / 1000 | 0,31 | 0,15 | no cupo | 0,48 |

Con lote 32 en la RTX 4070 Laptop — 0,59–0,84; en la RTX 2060 no cupo en la memoria.
**El umbral del 5% queda refutado** para esta implementación en ambas tarjetas (el criterio se había registrado antes del experimento).
La estimación anterior del 1,2–3,8% suponía activaciones de 8 bits y núcleos tensoriales; el perfil v2 necesita
activaciones de 16 bits, por lo que hay aproximadamente el doble de multiplicaciones.

O4 — en la RTX 2060 el perfil entero es 1,52–1,78 veces más lento que llama.cpp Q8_0 (b11960, el mismo modelo)
con lote 1 y 2,47–2,79 veces con lote 8. El umbral de 1,25 no se cumple.
Lo que de ello se deduce para la elección de la verificación lo analizó el consejo de modelos:
[STRATEGY_SEARCH](STRATEGY_SEARCH.md).

Limitaciones: entradas cortas y lote 1; núcleos enteros simples sin bloques tensoriales; el tiempo
de estas ejecuciones no es una medición de O3 y O4. A continuación, contexto largo de hasta miles de tokens,
núcleos rápidos con la misma aritmética y luego O3–O5.
