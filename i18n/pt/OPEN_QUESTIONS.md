<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Questões em aberto

[English](../../docs/OPEN_QUESTIONS.en.md) · [中文](../zh/OPEN_QUESTIONS.md) · [Español](../es/OPEN_QUESTIONS.md) · [Français](../fr/OPEN_QUESTIONS.md) · [Deutsch](../de/OPEN_QUESTIONS.md) · [Italiano](../it/OPEN_QUESTIONS.md) · [Русский](../../docs/OPEN_QUESTIONS.md) · **Português** · [العربية](../ar/OPEN_QUESTIONS.md)

Aqui estão reunidas as questões sem cuja solução a SkyNet não funcionará. Elas estão ordenadas
por importância. Para cada uma é indicado o que já se sabe e o que **já foi rejeitado**, para não
andar em círculos.

Uma boa contribuição: uma construção concreta, com as suposições declaradas abertamente, um ataque
a ela analisado e o custo calculado (por computação, memória, tráfego, registro na blockchain).
Ainda mais valiosa é uma brecha encontrada no projeto atual com um cenário concreto.

Parte das questões pode ser avançada por cálculo. Esses cálculos são executados pelo
[programa-agente](RESEARCH_AGENT.md) nos computadores de voluntários; a lista de tarefas e o seu
sentido estão descritos em [tasks/README.md](../../tasks/README.md), e o resumo dos resultados aparece
na pasta `results/`. No momento, as tarefas se referem às questões Q1, Q5 e Q9.

---

## Q1. Verificação barata em que a fraude é inútil mesmo com conluio

**A questão principal do projeto.** É preciso que um resultado falso não traga vantagem e que a
verificação custe alguns por cento do trabalho útil. Metas de referência: cerca de 5% para a
inferência, cerca de 20% para o treinamento (não comprovadas).

O que se sabe:

- Verificação por amostragem com confisco ou «pagamento apenas do verificado» dão uma garantia
  econômica até o limiar de conluio (veja [CURRENT_DESIGN, seção 3](CURRENT_DESIGN.md)). Elas não
  dão zero quando todos os verificadores da tarefa estão em conluio.
- A verificação de **cada** resultado pago dá zero com conluio. O recálculo custa +100% de trabalho.
  As provas criptográficas ainda são centenas e milhares de vezes mais caras do que o próprio trabalho.

Medições do piloto do projeto (em CPUs concretas, veja [PILOT_RESULTS](PILOT_RESULTS.md)):
a prova RISC Zero para uma linha da projeção do Qwen levou 22 minutos para ser construída; a execução
de um pacote de oito linhas na zkVM foi ~17 700 vezes mais longa do que a nativa; a repetição completa
da aritmética de uma linha na EVM custou 14,1 milhões de gas. O trabalho publicado FlashProve (2026)
relata 70–95× de tempo de GPU para o seu perfil inteiro de inferência.

O que procuramos: um esquema de verificação da inferência de LLM e de um passo de treinamento
(LoRA ou completo) cujo custo total (prover + verifier + dados + blockchain) caiba no orçamento, ou
uma prova de que isso é impossível para esta classe de problemas.

## Q2. Coincidência do resultado bit a bit em diferentes placas de vídeo

Todo o esquema de verificação se apoia na comparação exata. Com ponto flutuante, GPUs diferentes
somam em ordens diferentes e produzem bits diferentes; uma tolerância abre espaço para a fraude
«silenciosa» com um modelo barato.

Candidato: um modelo totalmente inteiro (pesos e ativações em int8, acumulação em int32, escalas por
multiplicador inteiro e deslocamento, não linearidades inteiras ou tabelas). Para o treinamento —
a decomposição em partes de oito bits (esquema de Ozaki).

Aberto: a qualidade do Qwen inteiro, a sua velocidade em GPUs de consumo (AMD, NVIDIA, Intel), o
treinamento inteiro. São necessários kernels concretos, uma estimativa da perda de qualidade e
trabalhos conhecidos.

## Q3. Disputa com recálculo na blockchain para o modelo completo

A disputa se estreita dividindo ao meio até uma única operação, que o contrato recalcula por si mesmo.
Isso foi construído apenas para uma linha do modelo (uma contestação bem-sucedida ~14 milhões de gas,
um jogo de 93 transações ~6 milhões de gas). São necessários: uma máquina inteira de referência para o
modelo completo, uma prova de que o jogo não pode ser desviado (substituir a entrada, o comprimento,
o caminho), os prazos dos lances, o preço sob carga e a escolha do blockchain ou de uma L2.

## Q4. O que aprender e como evitar que o modelo seja estragado

- Como a rede, sozinha e sem pessoas com direitos especiais, escolhe o plano de treinamento.
- Como se proteger de um sabotador disposto a perder créditos: falsificações não detectadas afetam
  imediatamente o treinamento.
- Como capturar backdoors ocultas de comportamento que o exame de qualidade não vê.
- Como verificar os conjuntos de dados no catálogo: um cálculo correto sobre dados nocivos não será
  corrigido pela verificação.

Uma garantia estreita conhecida: se o modelo base estiver congelado e a parte treinável mudar os
logits em no máximo `b`, então, onde a diferença entre os dois melhores tokens for maior que `2b`,
o envenenamento não mudará a resposta.

## Q5. Captura da maioria

O peso mede o trabalho, não a independência. O dono de mil GPUs alugadas parece mil participantes.
Um grupo com 3/4 do peso pode mudar as regras. São necessários mecanismos que limitem o dano de uma
maioria conquistada honestamente: um núcleo imutável, um limiar por modelos, regras de início fechado
e condições de abertura da rede.

## Q6. Privacidade das solicitações em dispositivos comuns

O dono do dispositivo pode ler a solicitação que ele computa. Dividir as camadas não ajuda: os vetores
ocultos são recuperados de volta. São necessárias: medidas parciais baratas, regras de acesso a
solicitações alheias, uma disputa sobre uma solicitação privada sem publicar dados intermediários e um
pagamento que não possa ser vinculado ao pagador.

## Q7. Disponibilidade dos dados

O verificador diz «não me deram os dados», quem armazena diz «eu dei», e o registro não viu a
transferência. Para dados pequenos, a publicação na blockchain ajuda; para dados grandes (o estado do
modelo) não há solução. Além disso: quantas cópias independentes são necessárias e como garantir que
estejam com donos diferentes.

## Q8. Resistência a bloqueios e primeira instalação

- Como um novato obtém o programa autêntico e o endereço do registro se as principais plataformas
  estiverem bloqueadas.
- Quais «pontos de encontro» públicos e independentes usar, para que não possam ser bloqueados por
  uma única decisão.
- Como trabalhar por meio de NAT e retransmissores sem servidores centrais.

## Q9. Economia

- A unidade de trabalho e a taxa pelo treinamento em que a emissão de créditos não os desvalorize
  até zero.
- Se a participação é vantajosa para os donos de grandes capacidades aos preços reais de eletricidade.
- A irregularidade da renda ao pagar apenas as tarefas verificadas.
- A compra e a venda de créditos por dinheiro e criptomoeda.

## Q10. Como um modelo que aprende sozinho seguirá as leis da SkyNet

O manifesto exige que o modelo não cause dano à humanidade nem ao ser humano, cumpra as solicitações
das pessoas dentro dos limites das leis superiores e preserve a si mesmo. Fixar de modo confiável
essas regras no modelo é um problema científico não resolvido, e em uma rede sem moderadores e com
autoaprendizado ele é ainda mais difícil. São necessários: como as leis entram no exame antes da
substituição da versão do modelo, como o treinamento não as dilui, quem decide e como são decididos
os casos controversos sem pessoas com direitos especiais, e como não transformar as leis em censura
de conhecimento útil.

---

## O que já foi rejeitado e por quê

| Ideia | Por que não serve |
|---|---|
| Pagar pelo tempo de trabalho ou pela potência declarada com base em relatórios e assinaturas | Um agente e um verificador em conluio assinam qualquer coisa; uma placa ociosa produz as mesmas mensagens |
| Tarefas curtas com verificação da resposta como prova de trabalho de uma placa de vídeo específica | A resposta pode ser calculada no computador de outra pessoa ou tirada do cache: o verificador vê dados idênticos |
| Depósito ou taxa de adesão | Proibido pelo requisito R5 |
| Multas sobre a conta disponível | Proibido pelo requisito R5 |
| Confiar em um único verificador honesto como garantia em caso de conluio total | Substitui o requisito R4 por uma suposição |
| Votação da maioria sobre a correção do resultado | A maioria pode ser capturada; a correção deve ser decidida pela aritmética |

Princípio geral: **se o caso honesto e o caso fictício dão ao verificador os mesmos dados, nenhum
algoritmo sobre esses dados os distinguirá.** Uma assinatura nova ou um registro na blockchain não
acrescentam tais dados. Por isso a rede paga pelo resultado verificável, e não pelo recurso.
