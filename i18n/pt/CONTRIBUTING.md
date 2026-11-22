# Como contribuir

[English](../../CONTRIBUTING.md) · [中文](../zh/CONTRIBUTING.md) · [Español](../es/CONTRIBUTING.md) · [Français](../fr/CONTRIBUTING.md) · [Deutsch](../de/CONTRIBUTING.md) · [Italiano](../it/CONTRIBUTING.md) · [Русский](../ru/CONTRIBUTING.md) · **Português** · [العربية](../ar/CONTRIBUTING.md)

Obrigado por querer ajudar. Aqui importa a precisão, não o volume: uma falha encontrada com um cenário concreto vale mais do que dez páginas de considerações gerais.

## O que trazer

- **Um ataque ao projeto atual.** Um cenário: quem age, o que faz, o que ganha, por que a rede não percebe. Indique a seção de [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md).
- **Uma solução para uma [questão em aberto](../../docs/OPEN_QUESTIONS.en.md).**
- **Uma fonte**: um artigo, protocolo ou projeto que resolva parte de um problema, com versão, data e o que ele **não** prova para o nosso caso.
- **Um cálculo de custo** ou a correção de um existente.
- **Uma correção de tradução**: uma imprecisão numa tradução da base (por meio do arquivo de errata).
- **Uma tarefa para o agente de pesquisa**: um cálculo que responda a parte de uma questão em aberto (veja [tasks/README.md](../../tasks/README.md)).
- **Capacidade de computação**: se você não tem assistente de IA nem tempo para escrever, rode o [agente de pesquisa](AGENT.md) no seu computador ou telefone.

## Como apresentar

Abra uma issue e comece o título com uma etiqueta:

| Etiqueta | Para |
|---|---|
| `[Attack]` | Uma forma de enganar ou perturbar a rede |
| `[Q<N>]` | Uma proposta para a questão em aberto N |
| `[Source]` | Um artigo ou projeto útil |
| `[Cost]` | Uma estimativa de custo ou correção de números |
| `[Translation]` | Uma imprecisão de tradução |
| `[Task]` | Um cálculo para o agente de pesquisa |

No texto, indique:

1. O que é garantido e sob quais suposições.
2. O mecanismo.
3. Os ataques conhecidos e o que resta.
4. O custo, marcado [cálculo] ou [medido].
5. Quais dos seis [requisitos](REQUIREMENTS.md) são cumpridos e quais não.

Pull requests para os documentos de trabalho (`docs/`) são bem-vindos. Se mudar o estado de um item, explique por quê. Issues e pull requests podem ser escritos em qualquer idioma do repositório.

## Regras

- **A base não muda.** Um pull request que altere o manifesto, os requisitos, o README ou suas impressões digitais não será aceito. Veja [CORE.md](../../CORE.md).
- Um cálculo não é apresentado como medição, nem uma proposta como decisão.
- Não publique chaves, senhas, dados pessoais ou endereços de computadores.
- Seja educado e objetivo. Critique ideias, não pessoas.

Se você trabalha com um assistente de IA, entregue a ele o [AGENTS.md](AGENTS.md). O autor de uma issue é responsável pela exatidão do seu texto.
