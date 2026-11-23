<!-- translation of docs/BOARD.md, source sha256: d39c7e244fa5cab003fbc95ca98c920aea26cdd80da02612e439942a53d37e14 -->

# Quadro de tarefas sem conta

[English](../../docs/BOARD.en.md) · [中文](../zh/BOARD.md) · [Español](../es/BOARD.md) · [Français](../fr/BOARD.md) · [Deutsch](../de/BOARD.md) · [Italiano](../it/BOARD.md) · [Русский](../../docs/BOARD.md) · **Português** · [العربية](../ar/BOARD.md)

Estado em 22 de novembro de 2026. Agente 0.2.0, lançado em 22 de novembro de 2026.

Até agora, um participante precisava de uma conta no GitHub para entregar um resultado. O quadro elimina isso: cada dispositivo cria a própria chave, e tudo o que ele diz à rede é um pequeno registro assinado com essa chave. Os registros passam por relays públicos do Nostr de diferentes donos e por nós completos operados por participantes. Ninguém precisa se registrar em lugar nenhum.

O GitHub permanece: a lista de tarefas assinada e os lançamentos do agente ainda são lidos do repositório, e a leitura não exige conta.

## O que um participante pode fazer

| Comando | O que faz |
|---|---|
| `skynet-agent net tasks` | Lista as tarefas do quadro com o estado delas |
| `skynet-agent net show ID` | Mostra uma tarefa com as declarações de trabalho em andamento e os relatórios, ou um relatório |
| `skynet-agent net post-task --title T --file F --accept A` | Publica uma tarefa de pesquisa; A diz o que um relatório deve conter |
| `skynet-agent net claim ID --hours H` | Diz "estou trabalhando nisto" por H horas |
| `skynet-agent net report ID --file F --summary S` | Entrega um relatório |
| `skynet-agent net accept ID` / `revise ID --note N` | O autor da tarefa julga um relatório |
| `skynet-agent net sync` | Busca novos registros e reenvia os ainda não entregues |
| `skynet-agent net id` | Mostra a chave pública deste dispositivo |

`ID` são os primeiros caracteres do identificador de um registro (pelo menos 6). Um nome de arquivo `-` lê o texto da entrada padrão, o que é conveniente para um assistente de IA. `--json` dá saída legível por máquina de `tasks` e `show`.

Os resultados de cálculo do [agente de pesquisa](RESEARCH_AGENT.md) saem do mesmo jeito: a configuração `submit_via` é `net` por padrão; `github` volta a usar os comentários do GitHub para enviar os resultados.

## Regras do quadro

1. **Declarar que se está trabalhando em uma tarefa não a reserva.** Qualquer pessoa pode entregar um relatório com ou sem declaração prévia. Portanto, uma declaração sem relatório não bloqueia ninguém; ela apenas informa aos outros que alguém está trabalhando.
2. **Só o autor da tarefa julga.** Um relatório é aceito ou devolvido apenas pela chave que assinou a tarefa. Na tarefa, o autor pode nomear até cinco suplentes; eles podem julgar relatórios depois de `handover_days` (14 por padrão) se o autor estiver ausente. O veredito do autor prevalece sobre o de um suplente; vale o veredito mais recente do autor.
3. **Cada dispositivo calcula o mesmo quadro a partir dos mesmos registros.** Não há servidor que decida. Um registro que não esteja assinado corretamente, pertença a outra rede ou esteja datado mais de um dia à frente é ignorado.
4. **Nada é apagado.** Um `revise` posterior reabre um relatório aceito; o histórico permanece.

## Onde os registros ficam

| Canal | Papel | Se falhar |
|---|---|---|
| 7 relays públicos do Nostr (listados em `agent/skynet_agent/trust.py`) | Carregam cada registro; verificado em 22.11.2026: aceitaram uma chave criada segundos antes | Um registro conta como entregue quando 2 relays ou 1 nó completo o confirmaram; os demais bastam |
| Nós completos (`node/receiver.py`) | Mantêm todo o histórico em disco e o entregam a qualquer pessoa por HTTP; puxam novos registros dos relays a cada 5 minutos | Qualquer participante pode iniciar outro; os relays continuam carregando os registros |
| O próprio dispositivo (`net/records.jsonl` na pasta do agente) | Sua própria cópia de tudo o que já viu | Buscada novamente dos relays e dos nós |

Os relays não prometem tempo de armazenamento. O histórico é mantido pelos nós completos e pelos dispositivos. Após uma parada total de tudo, a rede é encontrada novamente pelos endereços de relays e de nós embutidos no agente; é necessária pelo menos uma cópia sobrevivente.

## Limites honestos

- **Uma chave não custa nada.** Portanto, "várias chaves concordam" não prova nada, e o quadro pode ser enchido de lixo. Resultados de tarefas de cálculo que importam devem ser recalculados, não contados. É o mesmo problema da principal questão em aberto do projeto ([Q1](OPEN_QUESTIONS.md)), em miniatura.
- **Nada prova quem escreveu um texto primeiro.** Uma assinatura prova apenas qual chave publicou esses bytes.
- **Uma instalação nova não consegue distinguir o histórico mais novo de um mais antigo** se todas as fontes que ela consegue alcançar mostrarem o mais antigo.
- **Os relays podem recusar registros ou desaparecer.** Dois dos dez testados em 22.11.2026 não funcionaram, e os relays Git (GRASP) aceitam apenas registros sobre repositórios Git.
- **O arquivo de chave do agente é um arquivo comum.** Quem o copiar pode assinar como este dispositivo. A assinatura em Python puro não é de tempo constante.

## Executando um nó completo

Um nó completo precisa de Python 3.9+, um computador sempre ligado e, para ser útil aos outros, uma porta acessível pela internet. Ele não guarda nenhum segredo relevante e não tem direitos especiais.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` é um exemplo de unidade do systemd. O nó aceita no máximo 40 kB por registro, 60 registros por minuto de um endereço e para de crescer em `--max-mb`.