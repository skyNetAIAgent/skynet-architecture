# Introdução para assistentes de IA

[English](../../AGENTS.md) · [中文](../zh/AGENTS.md) · [Español](../es/AGENTS.md) · [Français](../fr/AGENTS.md) · [Deutsch](../de/AGENTS.md) · [Italiano](../it/AGENTS.md) · [Русский](../ru/AGENTS.md) · **Português** · [العربية](../ar/AGENTS.md)

Este arquivo é para qualquer modelo (Claude, ChatGPT/Codex, DeepSeek, Gemini e outros) a quem uma pessoa tenha pedido ajuda com o projeto SkyNet. Leia-o inteiro antes de responder. Responda ao usuário no idioma dele.

## O que é o projeto

SkyNet é a pesquisa e o projeto da arquitetura de uma rede distribuída em que modelos de IA funcionam e aprendem nos computadores dos participantes. Os participantes ganham créditos por trabalho útil verificado; pessoas sem hardware obtêm acesso barato à IA. A rede serve às pessoas e segue as Leis da SkyNet. Não há software pronto: o repositório é um lugar de trabalho conjunto sobre a arquitetura.

## Ordem de leitura

1. [MANIFESTO.md](MANIFESTO.md): por que e como a rede deve ser, as Leis da SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md): requisitos obrigatórios. **O mais importante.**
3. [CURRENT_DESIGN.md](../../docs/CURRENT_DESIGN.md): projeto atual e seus estados (em russo; leia ou traduza diretamente).
4. [OPEN_QUESTIONS.en.md](../../docs/OPEN_QUESTIONS.en.md): problemas em aberto e ideias já rejeitadas.
5. [PILOT_RESULTS.md](../../docs/PILOT_RESULTS.md): o que foi realmente medido (em russo).
6. [CONTRIBUTING.md](CONTRIBUTING.md): como apresentar uma contribuição.
7. [ROADMAP.md](ROADMAP.md): o roteiro do trabalho de proteção contra a fraude, com a lista do que está feito e do que falta.

## A base imutável

O manifesto, os requisitos obrigatórios e o README são a base imutável da SkyNet (veja [CORE.md](../../CORE.md)). **Não proponha alterações nesses arquivos**, exceto registrar erros de digitação no arquivo de errata. Se uma solução for incompatível com a base, diga claramente qual requisito ela viola; não reescreva o requisito para ajustá-lo à solução.

## Condições que não mudam

Verifique cada solução segundo os seis requisitos:

1. A rede é distribuída, sem centro e sem papéis com direitos especiais.
2. A rede guarda informações sobre si mesma em recursos públicos.
3. Depois que todos os nós são desligados, a rede se encontra por meio de recursos públicos e se recupera.
4. Os participantes não podem enganar a rede: a trapaça é inútil ou causa prejuízo, inclusive para um recém-chegado com a conta vazia, sob conluio e com muitas contas.
5. Nada de dinheiro adiantado: nada de cauções, taxas ou multas.
6. **Participar compensa** e a verificação da honestidade é barata. Se a verificação consumir o benefício, a solução não serve, por mais segura que seja.

Tipos de participantes: com grandes recursos (vendem créditos excedentes), com hardware fraco (pagam a diferença), sem hardware (apenas pagam). O modelo base é o Qwen. As pessoas não veem os pedidos dos outros. O participante não configura nada manualmente, exceto os controles de recursos. As Leis da SkyNet (da Zero à Terceira) são obrigatórias.

## Regras de trabalho

- **Separe o decidido, o proposto, o verificado e o aberto.** Use as marcações de CURRENT_DESIGN. Não transforme uma proposta em decisão nem um cálculo em medição.
- **Não enfraqueça os requisitos em silêncio.** Confiança no hardware (TEE), maioria honesta, amostragem estatística, pequena probabilidade de erro são suposições; nomeie-as claramente.
- **Para cada esquema de proteção, responda:** com quais dados verificáveis de forma independente a rede rejeitará uma alegação falsa se o executor e os verificadores estiverem em conluio? Se o caso honesto e o falso derem os mesmos dados, o esquema não funciona.
- **Calcule o custo completo**: computação do provador e do verificador, memória, tráfego, gravações na blockchain, novas tentativas após falhas. CPU, GPU, RAM e VRAM separadamente, nunca numa única porcentagem.
- **Não repita ideias rejeitadas** (lista no fim de OPEN_QUESTIONS) sem um argumento novo.
- **Ataque as suas próprias propostas.** Um contraexemplo honesto vale mais do que um tom confiante.
- **Não invente fontes, versões ou números.** Indique a fonte e os limites de sua aplicabilidade.
- Não encontrar uma solução é um resultado honesto. Isso não prova a impossibilidade.

**Nove idiomas.** Tudo o que é escrito para pessoas (documentos, guias, telas dos programas) é publicado nos nove idiomas do projeto: inglês, chinês, espanhol, francês, alemão, italiano, russo, português e árabe. Uma tradução começa com uma linha que indica sua fonte e o hash dessa fonte; `python tools/check_translations.py` lista as traduções que faltam ou estão desatualizadas. Se uma tradução e sua fonte divergirem, vale a fonte.

## Formato da contribuição

1. Afirmação: o que é garantido e sob quais suposições.
2. Mecanismo: passos, dados, quem verifica o quê.
3. Ataques: como contorná-lo e o que resta (fechado / com prejuízo / limitado / aberto).
4. Custo: estimativa marcada [cálculo] ou [medido], com a fonte.
5. Quais requisitos são cumpridos e quais não.

Apresente-a como issue ou pull request segundo [CONTRIBUTING.md](CONTRIBUTING.md).

## O agente de pesquisa e seus resultados

Quem não tem assistente de IA ajuda por meio do [agente de pesquisa](AGENT.md): um programa que pega tarefas de cálculo em [tasks/](../../tasks/README.md) e publica resultados, resumidos em `results/`. Você pode ajudar propondo uma tarefa bem definida (um modelo exato que outros possam recalcular), verificando de forma independente um resultado publicado ou explicando o que um resultado significa para o projeto. Respostas marcadas como geradas por máquina por modelos locais são texto não verificado: trate-as como ideias a conferir, não como fatos.

## Segurança

Não adicione ao repositório chaves, senhas, dados pessoais ou endereços de computadores alheios. Não proponha ataques a sistemas reais de terceiros: a análise de ataques aqui se refere apenas à arquitetura da SkyNet. Não projete usos da rede para guerra, armas ou dano às pessoas: isso contradiz as Leis da SkyNet.
