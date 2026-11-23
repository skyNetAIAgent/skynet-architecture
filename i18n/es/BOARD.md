<!-- translation of docs/BOARD.md, source sha256: d39c7e244fa5cab003fbc95ca98c920aea26cdd80da02612e439942a53d37e14 -->

# Tablero de tareas sin cuenta

[English](../../docs/BOARD.en.md) · [中文](../zh/BOARD.md) · **Español** · [Français](../fr/BOARD.md) · [Deutsch](../de/BOARD.md) · [Italiano](../it/BOARD.md) · [Русский](../../docs/BOARD.md) · [Português](../pt/BOARD.md) · [العربية](../ar/BOARD.md)

Estado el 22 de noviembre de 2026. Agente 0.2.0, publicado el 22 de noviembre de 2026.

Hasta ahora, un participante necesitaba una cuenta de GitHub para entregar un resultado. El
tablero elimina eso: cada dispositivo crea su propia clave, y todo lo que dice a la red es un
pequeño registro firmado con esa clave. Los registros viajan a través de retransmisores Nostr públicos
de distintos propietarios y de nodos completos mantenidos por los participantes. Nadie tiene que
registrarse en ninguna parte.

GitHub se mantiene: la lista de tareas firmada y las versiones del agente se siguen leyendo del
repositorio, y para leer no hace falta cuenta.

## Qué puede hacer un participante

| Comando | Qué hace |
|---|---|
| `skynet-agent net tasks` | Lista las tareas del tablero con su estado |
| `skynet-agent net show ID` | Muestra una tarea con los avisos de trabajo en curso y los informes, o un solo informe |
| `skynet-agent net post-task --title T --file F --accept A` | Publica una tarea de investigación; A dice qué debe contener un informe |
| `skynet-agent net claim ID --hours H` | Avisa «estoy trabajando en esto» durante H horas |
| `skynet-agent net report ID --file F --summary S` | Entrega un informe |
| `skynet-agent net accept ID` / `revise ID --note N` | El autor de la tarea juzga un informe |
| `skynet-agent net sync` | Recoge registros nuevos y reenvía los que aún no se han entregado |
| `skynet-agent net id` | Muestra la clave pública de este dispositivo |

`ID` son los primeros caracteres del identificador de un registro (al menos 6). Un nombre de
archivo `-` lee el texto de la entrada estándar, lo que resulta cómodo para un asistente de IA.
`--json` da una salida legible por máquina de `tasks` y `show`.

Los resultados de cálculo del [agente de investigación](RESEARCH_AGENT.md) salen por la misma
vía: el ajuste `submit_via` es `net` por defecto; `github` vuelve a usar los comentarios de GitHub para enviar los resultados.

## Reglas del tablero

1. **Avisar de que se está trabajando en una tarea no la reserva.** Cualquiera puede entregar un informe, haya avisado antes
   o no. Por tanto, un aviso sin informe no bloquea a nadie; solo avisa a los demás de que alguien
   está trabajando.
2. **Solo juzga el autor de la tarea.** Un informe solo puede aceptarlo o devolverlo la clave
   que firmó la tarea. En la tarea, el autor puede nombrar hasta cinco suplentes; estos pueden
   juzgar informes después de `handover_days` (14 por defecto) si el autor está ausente. El
   veredicto del autor prevalece sobre el de un suplente; cuenta el veredicto más reciente del
   autor.
3. **Cada dispositivo calcula el mismo tablero a partir de los mismos registros.** No hay
   ningún servidor que decida. Se ignora un registro mal firmado, que pertenezca a otra red o
   fechado con más de un día de adelanto.
4. **Nada se borra.** Un `revise` posterior reabre un informe aceptado; el historial se
   conserva.

## Dónde viven los registros

| Canal | Función | Si falla |
|---|---|---|
| 7 retransmisores Nostr públicos (listados en `agent/skynet_agent/trust.py`) | Transportan cada registro; comprobado el 22.11.2026: aceptaron una clave creada segundos antes | Un registro se considera entregado cuando lo confirmaron 2 retransmisores o 1 nodo completo; los demás bastan |
| Nodos completos (`node/receiver.py`) | Guardan todo el historial en disco y lo entregan a cualquiera por HTTP; recogen registros nuevos de los retransmisores cada 5 minutos | Cualquier participante puede levantar otro; los retransmisores siguen transportando los registros |
| El propio dispositivo (`net/records.jsonl` en la carpeta del agente) | Su propia copia de todo lo que ha visto | Se recoge de nuevo de retransmisores y nodos |

Los retransmisores no prometen ningún tiempo de conservación. El historial lo conservan los nodos
completos y los dispositivos. Tras una parada total de todo, la red se encuentra de nuevo mediante
las direcciones de retransmisores y nodos incorporadas en el agente; hace falta al menos una copia
superviviente.

## Límites honestos

- **Una clave no cuesta nada.** Por eso «varias claves respaldan el mismo resultado» no demuestra nada, y el
  tablero puede llenarse de basura. Los resultados de las tareas de cálculo que importan deben
  recalcularse, no contarse. Es el mismo problema que la principal pregunta abierta del proyecto
  ([Q1](OPEN_QUESTIONS.md)), en miniatura.
- **Nada demuestra quién escribió primero un texto.** Una firma solo demuestra qué clave publicó
  esos bytes.
- **Una instalación nueva no puede distinguir el historial más reciente de uno anterior** si
  todas las fuentes que puede alcanzar muestran esa versión anterior.
- **Los retransmisores pueden rechazar registros o desaparecer.** Dos de los diez probados el 22.11.2026
  no funcionaron, y los retransmisores de Git (GRASP) solo aceptan registros sobre repositorios Git.
- **El archivo de clave del agente es un archivo normal.** Quien lo copie puede firmar como este
  dispositivo. La firma en Python puro no es de tiempo constante.

## Ejecutar un nodo completo

Un nodo completo necesita Python 3.9+, un ordenador siempre encendido y, para ser útil a los
demás, un puerto accesible desde internet. No guarda ningún secreto relevante y no tiene derechos
especiales.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` es una unidad de ejemplo de systemd. El nodo admite como máximo 40 kB
por registro, 60 registros por minuto desde una dirección y deja de crecer al llegar a `--max-mb`.
