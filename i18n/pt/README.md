# SkyNet: projeto aberto da arquitetura

[English](../../README.md) · [中文](../zh/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · [Italiano](../it/README.md) · [Русский](../ru/README.md) · **Português** · [العربية](../ar/README.md)

## O que é este repositório

Aqui se projeta a arquitetura da SkyNet: uma rede distribuída em que modelos de IA funcionam e aprendem nos computadores dos participantes. Os participantes cedem à rede seus recursos de computação ociosos e recebem créditos em troca, enquanto pessoas sem hardware potente obtêm acesso barato à IA.

Este é um repositório de **pesquisa**. Aqui não há software pronto. Ele contém:

- o [manifesto](MANIFESTO.md): por que a rede é necessária, como ela deve ser e as Leis da SkyNet;
- os [requisitos obrigatórios](REQUIREMENTS.md), que não mudam;
- o [projeto atual da arquitetura](../../docs/CURRENT_DESIGN.md) com as marcações «decidido», «proposto» e «aberto» (em russo);
- as [questões em aberto](../../docs/OPEN_QUESTIONS.en.md) em que precisamos de ajuda (em inglês);
- [o que foi verificado no piloto](../../docs/PILOT_RESULTS.md) e o que não foi (em russo);
- as [regras de participação](CONTRIBUTING.md) e uma [introdução para assistentes de IA](AGENTS.md);
- o [agente de pesquisa](AGENT.md): um pequeno programa para quem não tem assistente de IA.

## Para quem

- **Engenheiros de sistemas distribuídos, criptógrafos, pesquisadores de ML.** Os principais problemas estão no cruzamento dessas áreas: verificação barata de computação, proteção contra conluio, recuperação de uma rede sem centro.
- **Proprietários de hardware** (placas de vídeo, servidores, PCs domésticos). A visão deles sobre lucro e custo de eletricidade é necessária para que a economia funcione na prática.
- **Quem trabalha com um assistente de IA.** Basta ao seu modelo (Claude, ChatGPT, DeepSeek e outros) ler o [AGENTS.md](AGENTS.md) para entrar no contexto e começar a trabalhar.
- **Quem simplesmente quer ajudar com o próprio computador ou telefone.** Não é preciso conhecimento especial: quem faz o trabalho é o [agente de pesquisa](AGENT.md).

## O sentido

Hoje nem todos têm acesso a uma IA potente: o preço, as restrições geográficas e políticas e o bloqueio de serviços atrapalham. Ao mesmo tempo, o mundo está cheio de placas de vídeo e computadores ociosos. A SkyNet deve unir as duas coisas: uma rede sem dono nem servidor central, difícil de desligar ou bloquear, que se encontra sozinha depois de um desligamento total, planeja o próprio treinamento, paga a cada um com justiça pelo trabalho útil verificado e serve às pessoas, não à guerra e à destruição.

## A parte mais difícil, com honestidade

A condição principal é que **enganar a rede seja inútil ou cause prejuízo, e que a verificação da honestidade seja barata**; caso contrário, participar não compensa. Uma solução que cumpra de forma comprovada essa condição sob conluio **ainda não existe**. Há candidatos fortes e dezenas de ataques analisados, mas os mecanismos-chave não foram construídos nem medidos. O estado atual está sempre descrito em [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) e [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md). Se você sabe resolver ao menos um desses problemas, precisamos de você.

## Como participar

1. Leia o [manifesto](MANIFESTO.md) e os [requisitos](REQUIREMENTS.md).
2. Escolha uma questão em [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) ou um ataque ao [projeto atual](../../docs/CURRENT_DESIGN.md).
3. Abra uma issue ou um pull request segundo as [regras](CONTRIBUTING.md). O mais valioso: uma falha encontrada com um exemplo concreto e uma solução com o custo calculado.

Se você trabalha com um assistente de IA, diga a ele: *«Estude este repositório seguindo o AGENTS.md e me ajude com a questão N de OPEN_QUESTIONS.»*

**Não tem assistente de IA?** Você pode ajudar mesmo assim. Instale o [agente de pesquisa SkyNet](AGENT.md): um pequeno programa de código aberto para Windows, macOS, Linux e Android. Ele consulta periodicamente este repositório, pega tarefas de pesquisa, calcula-as no seu dispositivo no tempo livre e publica os resultados. Ele se atualiza sozinho a partir deste repositório, e apenas para versões assinadas pelo projeto. A participação é voluntária: na etapa de pesquisa não há recompensas.

## A base imutável

O manifesto, os requisitos obrigatórios e este README formam a base imutável da rede (versão 1). Suas impressões digitais SHA-256 estão publicadas em [CORE_HASHES.txt](../../CORE_HASHES.txt). A edição canônica é a russa. Os detalhes estão no [manifesto](MANIFESTO.md) e em [CORE.md](../../CORE.md).

## Licença

Os textos da base são distribuídos sob CC BY-ND 4.0 (é permitido copiar, não é permitido distribuir versões modificadas); os demais documentos, sob CC BY 4.0. Veja [LICENSE](../../LICENSE).
