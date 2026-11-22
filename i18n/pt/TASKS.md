<!-- translation of tasks/README.md, source sha256: f0685cfe87baef739cff7ff9121f8ab2fd0aed86866b5638fd79dcdd347c1916 -->

# Tarefas para agentes de pesquisa

[English](../../tasks/README.md) · [中文](../zh/TASKS.md) · [Español](../es/TASKS.md) · [Français](../fr/TASKS.md) · [Deutsch](../de/TASKS.md) · [Italiano](../it/TASKS.md) · [Русский](../ru/TASKS.md) · **Português** · [العربية](../ar/TASKS.md)

Esta pasta guarda o trabalho que os [agentes de pesquisa](../../agent/README.md) realizam:

- [`index.json`](../../tasks/index.json): a lista atual de tarefas;
- `index.json.sig`: a assinatura dela (os agentes ignoram uma lista sem uma assinatura válida);
- [`context/`](../../tasks/context): textos congelados que as perguntas de IA citam.

Os resultados aparecem como comentários na issue de acompanhamento de cada tarefa e são
resumidos em [`results/`](../../results) por `tools/collect_results.py`.

## O que é uma tarefa

Uma tarefa é dado: o nome de um cálculo embutido no agente (um "kernel"), os
parâmetros dele e o número de porções independentes (`units`) em que o trabalho é dividido.
Uma tarefa não pode conter código. Um novo tipo de cálculo exige uma nova versão assinada do
agente.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

Não há escalonador. Cada agente escolhe uma porção aleatória que ainda não fez. Que vários
agentes caiam na mesma porção é intencional: todos os kernels de cálculo são aritmética
inteira exata, de modo que trabalho igual produz dígitos iguais em qualquer dispositivo, e
uma porção conta como confirmada quando `redundancy` contas diferentes do GitHub publicam o
mesmo hash. Hashes diferentes para uma mesma porção são um conflito que um mantenedor resolve
recalculando-a.

## Kernels no agente 0.1

| Kernel | O que calcula | Fonte |
|---|---|---|
| `selftest@1` | Uma carga de trabalho inteira fixa; todo dispositivo deve devolver o mesmo resumo | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Pagamento esperado exato de um participante que envia resultados falsos e sai, em uma família de estratégias; relata as estratégias que superam a saída honesta | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Probabilidade exata de um mês ou trimestre de prejuízo quando apenas tarefas verificadas são pagas | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Opcional: uma pergunta para um modelo local de IA que o participante executa | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

Cada arquivo-fonte começa com o modelo exato que implementa, para que qualquer pessoa possa
recalcular um resultado de forma independente.

## As tarefas publicadas agora, e por quê

Todas dizem respeito à principal questão em aberto do projeto: é possível tornar a trapaça
inútil a baixo custo ([OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)).

| Tarefa | Pergunta |
|---|---|
| `selftest-1` | O pipeline funciona no seu dispositivo? |
| `exit-a-honest-check` | Sem conluio, existe alguma forma de lucrar com resultados falsos antes de sair? O projeto diz que não |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | Com tarefas pequenas iguais: a partir de que parcela de verificadores em conluio sair com resultados falsos compensa? A estimativa do projeto é de cerca de 91% |
| `exit-a-uniform-cap-h399` | O mesmo com o limite proposto "no máximo um terço do valor pendente em trabalho", em três ondas |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | O mesmo quando as tarefas podem ter qualquer tamanho, com e sem esse limite |
| `lottery-b-table` | Se apenas tarefas verificadas são pagas, com que frequência um participante pequeno tem um mês de prejuízo? |
| `ask-variant-b-attack` | Para modelos locais de IA: encontrar um novo ataque a "a rede paga apenas pelo trabalho verificado" |

São cálculos sobre as regras como escritas nos documentos de projeto. Não são medições de
hardware nem experimentos com a rede. As tarefas de medição (por exemplo, se a inferência
inteira dá os mesmos bits em placas de vídeo diferentes) só serão publicadas depois que os
mantenedores do projeto abrirem experimentos.

## Propor uma tarefa

Abra uma issue intitulada `[Task] …` e diga:

1. a pergunta que o cálculo responde e a qual questão em aberto ela pertence;
2. o modelo exato, para que possa ser recalculado de forma independente;
3. qual kernel e quais parâmetros fariam isso, ou o que um novo kernel deve calcular;
4. como um resultado errado ou forjado seria percebido.

Os mantenedores verificam a tarefa com `tools/sign_tasks.py --check`, adicionam-na ao
`index.json` e assinam a lista. Somente o detentor da chave de lançamento pode assinar; veja
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
