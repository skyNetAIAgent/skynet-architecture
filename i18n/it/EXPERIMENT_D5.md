<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 8344ba8a8a4752fc05abdf96a28bee33a5bbf79f5b62c3aa773ea9041db4a33a -->

# Esperimento D5: Qwen3.5-4B intero

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · [Français](../fr/EXPERIMENT_D5.md) · [Deutsch](../de/EXPERIMENT_D5.md) · **Italiano** · [Русский](../../docs/EXPERIMENT_D5.md) · [Português](../pt/EXPERIMENT_D5.md) · [العربية](../ar/EXPERIMENT_D5.md)

Stato al 25 novembre 2026: **primi risultati sugli input corti (sezione 7); contesto lungo,
velocità e qualità non sono ancora misurati.** L'esperimento è autorizzato dalla decisione D5
([ROADMAP](ROADMAP.md), sezione 3) e fa parte della fase 5 della tabella di marcia. Esso verifica la principale ipotesi non misurata
del miglior candidato della fase 4 — la verifica della risposta da parte del pagatore stesso (PPS,
[VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sezioni 3.2 e 5.2).

## 1. Che cosa si verifica

Il pagatore che dispone del modello deve, in un solo passaggio, ricalcolare la richiesta e la risposta ottenuta
e ottenere **gli stessi identici bit** che l'esecutore ottiene alla generazione. Ciò è possibile solo se tutta
l'aritmetica del modello è definita con numeri interi e un arrotondamento fissato: la somma di interi non dipende
dall'ordine dell'addizione, finché non c'è overflow. L'esperimento risponde a cinque domande; i criteri
di confutazione sono fissati prima dell'avvio:

| Esperimento | Domanda | Che cosa lo confuta |
|---|---|---|
| O1 | Coincidono i bit su schede video diverse e sul processore | Almeno un bit diverso dei logit, del token scelto, del motivo di arresto o degli hash di controllo a parità di input. Prima della conclusione — ricerca della prima divergenza e ripetizione sull'input più corto. La conclusione riguarda solo i dispositivi provati e la versione dell'implementazione |
| O2 | Coincidono i bit nella decodifica punto per punto e nel passaggio dell'intera sequenza pronta su una scheda | Qualsiasi bit diverso, compreso l'hash dello stato ricorrente degli strati Gated DeltaNet nei punti di controllo |
| O3 | Quanto costa la verifica della risposta rispetto alla sua generazione | La mediana della quota `ρ(1)` è maggiore del 5% almeno per una delle quattro coppie di lunghezze di richiesta e risposta nominate in anticipo con pacchetto 1. I pacchetti 8 e 32 si misurano separatamente |
| O4 | Quanto il profilo intero è più lento di quello normale a 8 bit sulla stessa scheda | La mediana del rallentamento è maggiore di 1,25 volte in una cella comparabile (soglia diagnostica: decidono O3 e O5) |
| O5 | Quanta qualità si perde | La perdita di accuratezza è maggiore di 3 punti percentuali su 320 compiti scelti in anticipo (64 da ciascuna delle quattro sezioni di MMLU e dal MGSM russo) rispetto al profilo normale a 8 bit dello stesso modello |

I 1,2–3,8% calcolati nella fase 4 non sono considerati un risultato di O3: solo questo esperimento li conferma o li confuta.

## 2. Modello e attrezzatura

- **Modello:** repository ufficiale Qwen/Qwen3.5-4B su Hugging Face, revisione fissata
  `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Due file di pesi da 5 329 398 688 e 3 990 429 408
  byte, in totale circa 9,3 GB. Dopo il download si confrontano gli SHA-256 dell'inventario del repository.
- **Architettura** (secondo il `config.json` pubblicato): 32 blocchi, vettore nascosto 2560, MLP 9216.
  Ogni quarto blocco (indici 3, 7, …, 31) — attenzione completa: 16 teste di query, 4 teste
  di chiavi e valori, dimensione della testa 256, gate di uscita, rotazione delle prime 64 coordinate. Gli altri
  24 blocchi — Gated DeltaNet: stato ricorrente 32 × 128 × 128 per blocco, convoluzione causale
  di profondità 4. Vocabolario 248 320, matrici di input e di output condivise. L'«INT-canone» transformer
  normale della fase 4 non è sufficiente per questo modello; il profilo viene definito di nuovo (sezione 3).
- **Dispositivi:** RTX 2060 6 GB (Turing) sul Linux domestico dell'accompagnatore; RTX 4070 Laptop
  8 GB (Ada) sul computer del proprietario; il processore come terzo esecutore indipendente. Con il consenso —
  i dispositivi di altri partecipanti tramite mini-agente.
- **Memoria** [calcolo]: i pesi principali a 8 bit — 4010 MiB. Con pacchetto 1 e lunghezza fino a 3000 token
  tutto entra in 6 GB; il pacchetto 32 con lunghezza 3000 richiede circa 7064 MiB già prima dei buffer di lavoro
  e sulla RTX 2060 è possibile solo con il trasferimento della storia nella memoria operativa.

## 3. Profilo intero

Il profilo riceve un nome e una versione separati e viene congelato prima di O1–O5. La base è il grafo numerico
del progetto ChatGPT con le correzioni di entrambi i critici:

1. **Pesi e attivazioni.** Pesi a 8 bit per riga, la scala della riga è un numero binario esatto.
   Attivazioni a 16 bit in virgola fissa (1024 = unità). L'arrotondamento è unico per tutte le
   operazioni: al più vicino, la metà al pari, in modulo con restituzione del segno.
2. **Normalizzazioni e non linearità** (RMSNorm, L2, SiLU, sigmoide, softplus, esponenziale) — formule
   intere con radice quadrata intera e tabelle. Le tabelle sono costruite fuori dal programma con arrotondamento
   dimostrato corretto (MPFR) e pubblicate con SHA-256.
3. **Attenzione completa.** Punteggi, esponenziale da tabella, quote a 16 bit. Il critico ChatGPT ha trovato
   nel progetto iniziale un errore: a parità di valori, l'aggiunta di un'altra chiave uguale
   cambiava l'uscita da 1365 a 683. Correzione: dividere la somma ponderata per la somma delle quote arrotondate
   stesse, così un valore costante si conserva esattamente.
4. **Gated DeltaNet.** Decadimento, correzione e aggiornamento dello stato — cinque assegnazioni intere
   per ogni token in un unico ordine canonico nel tempo. La formula del progetto DeepSeek
   descriveva un'altra ricorsione ed è stata respinta. La forma «a blocchi» accelerata è ammessa solo
   se riproduce gli stessi bit su ogni token.
5. **Scelta del token.** Massimo sulla coppia (punteggio, −numero) su tutto il vocabolario, in modo greedy. Modalità separata —
   Gumbel-max canonico con pseudocasualità HMAC-SHA256 dal seme della richiesta (D22).
   Arresto — la prima causa: EOS o limite.
6. **Limiti di overflow** sono fissati per ogni accumulatore; dove 32 bit non bastano, si usano 64.
   Test separati verificano i valori estremi.

Tutti i punti ambigui («bivi») si chiudono prima del primo avvio leggendo il sorgente del modello
della versione fissata di Transformers; l'hash di questo sorgente entra nel manifesto del profilo.

## 4. Ordine dei lavori

1. **P0, preparazione (2–4 giorni).** Download e verifica del modello; elenco di tutti i tensori; chiusura
   dei bivi secondo il sorgente; tabelle; vettori di controllo con valori manuali.
2. **Passo ridotto (1–1,5 settimane).** Riferimento sul processore per tutto il modello su input corti;
   confronto con il calcolo normale in virgola mobile (solo per cogliere un errore di importazione,
   non per O1/O2). Versione semplice per la scheda video senza unità tensoriali. Le risposte di O2 su una scheda
   e di O1 «processore contro RTX 2060» su contesto corto. Poi lo stesso pacchetto sulla RTX 4070
   Laptop — la prima risposta di O1 per due schede video diverse.
3. **Passo completo (3–4 settimane).** Moltiplicazioni veloci a 8 bit, kernel fuso della ricorsione DeltaNet,
   pacchetti 1/8/32, esperimenti O3, O4, O5, ripetizione sul secondo dispositivo.

Tutto il lavoro si svolge in una directory separata sul Linux domestico, con un ambiente Python
proprio (CuPy con le librerie CUDA 12 dai pacchetti pip, senza installazione di sistema). I servizi in funzione
e le directory di altri esperimenti non vengono toccati. La stima complessiva è di 4–6 settimane di lavoro di un solo
sviluppatore; i rischi principali sono il costo della ricorsione DeltaNet (lo mostrerà O3), le ambiguità
prima di P0 e il supporto di Qwen3.5 nei motori comuni per O4/O5.

## 5. Che cosa sarà pubblicato

Per ogni avvio: manifesto del profilo e delle versioni, input, hash dei logit e degli stati per strato,
tempi grezzi e condizioni di misurazione, guasti iniziali insieme alle correzioni. La coincidenza dei bit
riguarda solo i dispositivi e le versioni provati. Il risultato di ogni esperimento è inserito nella tabella di marcia
(fase 5) e in questo documento; l'esperimento è considerato concluso quando lo ha ripetuto un secondo partecipante.

## 6. Chi ha fatto che cosa

- **Progetti dell'esperimento:** due progetti indipendenti — ChatGPT e DeepSeek.
- **Critica incrociata:** ChatGPT ha analizzato entrambi i progetti, DeepSeek ha analizzato entrambi i progetti;
  ricalcoli della memoria e dei limiti, verifica della ricorsione corta e della correzione dell'attenzione su piccole enumerazioni.
- **Sintesi e decisioni sul piano:** Claude.

- **Preparazione, profili v1 e v2, riferimento sul processore e versione per la scheda video:** ChatGPT.
- **Verifiche indipendenti:** DeepSeek — importazione del modello con il forward ufficiale, univocità
  e limiti di overflow del profilo v2.
- **Esecuzioni sulle schede video e verifica dei risultati:** Claude (dalla sandbox dei modelli la scheda video
  non è accessibile).

## 7. Risultati

**24 novembre 2026, input corti.** Input: due storie da 8 + 8 token e sei testi brevi (russo, inglese,
cinese, aritmetica, codice, ricetta), profondità 4 e 32 blocchi; pacchetto 1.

- **Importazione del modello.** Il calcolo normale in virgola mobile, scritto secondo il sorgente, ha coinciso
  con il forward ufficiale di Transformers 5.24.0: lo stesso token scelto in 130 posizioni su 130,
  scostamento dei logit non superiore a 3,6·10⁻⁵ (verificato da ChatGPT e indipendentemente da DeepSeek).
- **Profilo v1 respinto.** Esso era riproducibile bit per bit, ma la scala 1/1024 era troppo grossolana:
  l'uscita della ricorsione DeltaNet veniva quasi interamente arrotondata a zero, la coincidenza del token
  scelto con il modello — 5 su 8, la correlazione dei logit circa 0,8.
- **Profilo v2** (attivazioni con esponente binario per vettore e mantissa a 16 bit, residuo e stato
  della ricorsione con passo 2⁻²⁰, chiavi e valori dell'attenzione a 32 bit): lo stesso token del modello
  ufficiale in 90 posizioni su 90, correlazione media dei logit 0,9996, minima 0,998. Lo stato e la cache
  occupano 238 MiB con 3000 posizioni contro 95 del v1; il numero di moltiplicazioni per token è lo stesso —
  4,2 miliardi.
- **O2 (un solo dispositivo).** La generazione token per token e il passaggio sulla risposta pronta con
  suddivisione in 1, 3 e 8 posizioni danno gli stessi bit di tutti i logit, dei token scelti e degli hash
  degli stati.
- **O1 (dispositivi diversi).** Processore (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) e RTX 4070
  Laptop (Ada, Windows, CuPy): 88 confronti su ciascuna scheda, 242 360 320 logit, 976 token scelti
  e 37 152 hash di stato per scheda — **nessuna differenza**.

Limiti: input corti e pacchetto 1; kernel interi semplici senza unità tensoriali; il tempo di queste
esecuzioni non è una misurazione di O3 e O4. In seguito — contesto lungo fino a migliaia di token,
kernel veloci con la stessa aritmetica, poi O3–O5.
