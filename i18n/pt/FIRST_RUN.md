<!-- translation of results/FIRST_RUN.md, source sha256: 786aa2e462922d0a3a2ec06d0da0e26d246a2563867e215a11cfbf5a799bfe0a -->

# Primeira execução da primeira lista de tarefas (num único computador, com resultados ainda não confirmados)

[English](../../results/FIRST_RUN.md) · [中文](../zh/FIRST_RUN.md) · [Español](../es/FIRST_RUN.md) · [Français](../fr/FIRST_RUN.md) · [Deutsch](../de/FIRST_RUN.md) · [Italiano](../it/FIRST_RUN.md) · [Русский](../ru/FIRST_RUN.md) · **Português** · [العربية](../ar/FIRST_RUN.md)

Em 22 de novembro de 2026, cada unidade da lista de tarefas número 1 foi calculada uma vez em um
único computador Windows com o mesmo código que os agentes executam: 702 unidades, 15,5 horas de
CPU, nenhuma falha. Um computador não é uma confirmação. Os números abaixo só se tornam resultados
do projeto quando outros participantes publicam os mesmos hashes (veja [README.md](RESULTS.md)).

## Saindo com resultados falsos (kernel `exit-scam-a@1`, variante A do projeto)

Um participante com um valor H0 "pendente" envia resultados falsos em algumas ondas rápidas e
sai. Se simplesmente saísse, receberia H0. A tabela mostra a menor parcela de verificadores em
conluio a partir da qual alguma estratégia da família pesquisada tem um retorno esperado acima
de H0. O modelo exato está no topo de
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py).

| Tarefa | Estratégias examinadas | Lucrativa a partir da parcela de conluio | Melhor retorno esperado ali |
|---|---:|---|---|
| `exit-a-honest-check`: sem conluio, qualquer tamanho de tarefa, duas ondas | 92 169 600 | nunca | 0,980 × H0 |
| `exit-a-uniform-h399`: tarefas pequenas iguais, 399 preços pendentes, uma onda | 7 600 | 0,892 (não em 0,890) | 1,0066 × H0 |
| `exit-a-uniform-h1200`: tarefas pequenas iguais, 1200 preços pendentes, uma onda | 22 800 | 0,908 (não em 0,906) | 1,0117 × H0 |
| `exit-a-uniform-cap-h399`: tarefas pequenas iguais, três ondas, "no máximo um terço em trabalho" | 71 772 196 | 0,890 (não em 0,888) | 1,0059 × H0 |
| `exit-a-sizes-cap`: qualquer tamanho de tarefa, três ondas, "no máximo um terço em trabalho" | 1 190 974 992 | 0,875 (não em 0,870) | 1,00004 × H0; 1 034 × H0 em 0,880 |
| `exit-a-sizes-nocap`: qualquer tamanho de tarefa, duas ondas, sem esse limite | 69 148 800 | 0,800 (não em 0,780) | 1 218 × H0; 4,91 × H0 em 0,850 |

O que isso sugere:

- A estimativa do projeto "trapacear dá prejuízo enquanto os que estão em conluio detiverem menos
  de cerca de 91%" vem da média sobre uma única falsificação. Ela não conta que um participante
  pode perder, no máximo, o valor pendente (não há depósitos nem multas). Para quem sai, a perda
  tem limite e o ganho não, o que reduz o limiar para cerca de 87,5–89%.
- A regra proposta "no máximo um terço do valor pendente em trabalho de uma vez" é necessária.
  Sem ela, as recompensas não verificadas da primeira onda aumentam o valor pendente e permitem
  tarefas maiores na segunda onda, e o limiar cai para cerca de 80%.
- Sem conluio, não foi encontrada nenhuma forma lucrativa de sair com resultados falsos.

Limites: isto é um cálculo em um modelo formal das regras, não uma medição; a busca cobre apenas
as famílias listadas; a grade de parcelas de conluio tem passos de 0,002 a 0,02.

## Pagando apenas por tarefas verificadas (kernel `lottery-b@1`, variante B do projeto)

Probabilidade de a renda de um período ficar abaixo do custo do trabalho feito nele, quando uma
tarefa é verificada com probabilidade 1/P e uma tarefa verificada é paga pelo equivalente a P vezes o preço da tarefa. Somas
binomiais exatas.

| Tarefas por mês | Verificadas | Custo / preço | Meses com prejuízo | Trimestres com prejuízo |
|---:|---|---:|---:|---:|
| 600 | 1 em 10 | 95% | 32,20% | 22,91% |
| 6 000 | 1 em 100 | 95% | 33,10% | 24,02% |
| 6 000 | 1 em 100 | 80% | 4,84% | |
| 60 000 | 1 em 100 | 95% | 10,47% | 1,55% |
| 200 000 | 1 em 100 | 95% | 1,15% | |
| 200 000 | 1 em 100 | 98% | 18,15% | |
| 600 | 1 em 100 | 95% | 44,49% | |

Com 600 tarefas por mês e 1 em 100 verificadas, nada é pago em 0,24% dos meses. A tabela completa
tem 360 células; ela aparecerá em `summary.json` assim que os agentes a publicarem.
