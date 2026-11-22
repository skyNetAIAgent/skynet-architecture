# Requisitos obrigatórios da SkyNet

[English](../../REQUIREMENTS.md) · [中文](../zh/REQUIREMENTS.md) · [Español](../es/REQUIREMENTS.md) · [Français](../fr/REQUIREMENTS.md) · [Deutsch](../de/REQUIREMENTS.md) · [Italiano](../it/REQUIREMENTS.md) · [Русский](../ru/REQUIREMENTS.md) · **Português** · [العربية](../ar/REQUIREMENTS.md)

*Versão 1, 22 de novembro de 2026. Edição canônica, parte da base imutável da SkyNet. Tradução para o português; o [texto russo](../ru/REQUIREMENTS.md) é o canônico.*

Estes requisitos, junto com o [manifesto](MANIFESTO.md) e as Leis da SkyNet, formam a **base imutável da rede**: não podem ser alterados por votação, nem por decisão dos criadores, dos desenvolvedores ou da maioria dos participantes. Uma solução que viole mesmo um único requisito não serve para a SkyNet. Ela pode ser discutida como pesquisa, mas com a indicação clara de qual requisito viola.

## As seis condições principais

| N.º | Requisito | Como verificar uma solução |
|---|---|---|
| R1 | **A rede é distribuída.** | Dispositivos de diferentes participantes mantêm juntos o seu funcionamento. A perda de qualquer nó, de qualquer servidor, inclusive de um pertencente aos criadores do projeto, ou de um site de publicação não impede os demais de continuar. |
| R2 | **A rede guarda informações sobre si mesma em recursos públicos.** | O software instalado obtém do exterior informações suficientes para reconhecer a rede e encontrar os nós que retornam. Essas informações sobrevivem ao desligamento simultâneo de todos os nós. Há várias fontes. |
| R3 | **A rede se encontra e se recupera após um desligamento total.** | Os programas que retornam se encontram sozinhos por meio de recursos públicos, sem o endereço de um coordenador ativo e sem uma lista manual de nós. |
| R4 | **Os participantes não podem enganar a rede.** | Uma alegação falsa não leva a um resultado aceito, aos poderes de outrem, a uma recompensa indevida nem a uma história reescrita. Conluio e contas múltiplas (Sybil) são levados em conta. Para cada solução, mostra-se com quais dados verificáveis de forma independente a rede rejeitará uma alegação falsa. **Sentido prático:** a trapaça é inútil ou causa prejuízo, inclusive para um recém-chegado com a conta vazia. |
| R5 | **Nada de dinheiro adiantado.** | Nada de taxas, cauções ou multas cobradas da conta. Cauções e multas afastam os participantes. |
| R6 | **Participar compensa.** | Fornecer recursos (GPU, VRAM, CPU, RAM, SSD, HDD) é lucrativo. A verificação da honestidade é barata: seu custo serve a todos, especialmente aos donos de grandes equipamentos e de eletricidade cara. |

**R6 é o mais importante.** Se a verificação da honestidade exigir muita computação, participar deixa de compensar e a rede perde o sentido.

## Tipos de participantes

| Participante | O que faz |
|---|---|
| Com grandes recursos | Ganha créditos suficientes para as próprias necessidades e vende o excedente a outros participantes |
| Com hardware fraco | Ganha menos do que gasta com os modelos da rede e paga a diferença em criptomoeda ou dinheiro |
| Sem hardware | Apenas consumidor: paga para usar os modelos |

A mesma pessoa pode ser fornecedora de recursos e usuária.

## Outras condições adotadas

- **O estado é preservado.** Direitos confirmados, obrigações, o histórico das tarefas aceitas, a última versão aceita do modelo e os dados para retomar o treinamento sobrevivem a uma parada total. Repetir um passo inacabado não dá uma segunda recompensa.
- **Divisão da rede.** Quando os históricos se contradizem, os créditos em disputa aguardam o histórico canônico. Uma mesma contribuição nunca é paga duas vezes.
- **Sites e chaves substituíveis.** A perda de uma conta, espelho ou chave não impede para sempre a recuperação.
- **Decisões verificáveis após reinício.** Para créditos, mudanças de regras e aceitação de uma versão do modelo, guardam-se dados com os quais qualquer nó pode verificar o fundamento da decisão.
- **Mínimo público.** O catálogo aberto contém apenas o necessário para a descoberta e a verificação de autenticidade. Chaves privadas, pedidos privados e dados pessoais não são publicados.
- **Privacidade.** As pessoas não veem os pedidos nem os dados pessoais dos outros.
- **Independência de indivíduos.** Ninguém tem direitos especiais, nem mesmo o desenvolvedor. A rede define e altera o próprio plano de treinamento; é permitida a votação sobre uma lista de opções.
- **Simplicidade para o participante.** O participante não escolhe nada manualmente: instala o programa, aceita os termos, ajusta os controles de recursos e aperta «Iniciar».
- **Limites de recursos separados.** CPU, GPU, RAM, VRAM e disco são limitados separadamente; não podem ser somados numa única porcentagem.
- **Toda a capacidade livre treina.** A capacidade não ocupada por pedidos vai para o treinamento.
- **Modelo base.** No início, Qwen com pesos abertos e licença livre. Só é possível mudar para outro modelo com pesos abertos e licença livre.
- **Leis da SkyNet.** As quatro leis do [manifesto](MANIFESTO.md) vinculam tanto o comportamento do modelo quanto as regras da rede. A rede serve às pessoas e não é construída como instrumento de guerra.

## O que não pode substituir os requisitos

- Tempo de funcionamento, número de relatórios e período de checkpoints **não** são fundamento de pagamento.
- A assinatura de um participante, mesmo junto com a de outro nó, **não** prova que um recurso foi fornecido: quem está em conluio assina qualquer coisa.
- Amostragem estatística, confiança num enclave de hardware (TEE) ou um pequeno erro criptográfico são suposições. Podem ser propostas, mas devem ser nomeadas claramente, e não apresentadas como cumprimento de R4.
- Um teste bem-sucedido não prova proteção contra trapaça.
