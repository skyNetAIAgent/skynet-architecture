<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Questioni aperte

[English](../../docs/OPEN_QUESTIONS.en.md) · [中文](../zh/OPEN_QUESTIONS.md) · [Español](../es/OPEN_QUESTIONS.md) · [Français](../fr/OPEN_QUESTIONS.md) · [Deutsch](../de/OPEN_QUESTIONS.md) · **Italiano** · [Русский](../../docs/OPEN_QUESTIONS.md) · [Português](../pt/OPEN_QUESTIONS.md) · [العربية](../ar/OPEN_QUESTIONS.md)

Qui sono raccolti i problemi senza la cui soluzione SkyNet non potrà funzionare. Sono ordinati per importanza. Per ciascuno è indicato ciò che è già noto e ciò che è **già stato respinto**, per non girare in tondo.

Un buon contributo: una costruzione concreta, le assunzioni dichiarate apertamente, l'attacco a essa analizzato, il costo calcolato (in calcoli, memoria, traffico, scritture nella blockchain). Ancora più preziosa è una falla trovata nel progetto attuale con uno scenario concreto.

Una parte delle questioni può essere portata avanti con il calcolo. Tali calcoli sono eseguiti dall'[agente di ricerca](RESEARCH_AGENT.md) sui computer dei volontari; l'elenco dei compiti e il loro significato sono descritti in [tasks/README.md](../../tasks/README.md), il riepilogo dei risultati compare nella cartella `results/`. Al momento i compiti riguardano le questioni Q1, Q5 e Q9.

---

## Q1. Verifica a basso costo in cui l'inganno è inutile anche in caso di collusione

**La questione principale del progetto.** Occorre che un risultato falso non porti alcun beneficio e che la verifica costi una piccola percentuale del lavoro utile. Obiettivi indicativi: circa il 5% per l'inferenza, circa il 20% per l'addestramento (non confermati).

Cosa è noto:

- La verifica a campione con penalizzazione, o «pagare solo ciò che è stato verificato», dà una garanzia economica fino alla soglia di collusione (vedi [CURRENT_DESIGN, sezione 3](CURRENT_DESIGN.md)). Non dà lo zero in caso di collusione di tutti i verificatori del compito.
- Lo zero in caso di collusione lo dà la verifica di **ogni** risultato pagato. Il ricalcolo costa il +100% del lavoro. Le prove crittografiche per ora sono centinaia e migliaia di volte più costose del lavoro stesso.

Misurazioni dal progetto pilota (su CPU concrete, vedi [PILOT_RESULTS](PILOT_RESULTS.md)): la prova RISC Zero per una riga della proiezione Qwen è stata costruita in 22 minuti; l'esecuzione di un lotto di otto righe nella zkVM è risultata ~17 700 volte più lenta del nativo; il ricalcolo completo dell'aritmetica di una riga nell'EVM è costato 14,1 milioni di gas. Il lavoro pubblicato FlashProve (2026) riporta 70–95× di tempo GPU per il proprio profilo di inferenza intero.

Cosa cerchiamo: uno schema di verifica dell'inferenza di un LLM e di un passo di addestramento (LoRA o completo) il cui costo totale (prover + verifier + dati + blockchain) rientri nel budget, oppure una prova che per questa classe di problemi ciò sia impossibile.

## Q2. Coincidenza del risultato bit a bit su schede video diverse

L'intero schema di verifica si regge su un confronto esatto. Con i numeri in virgola mobile GPU diverse sommano in ordine diverso e producono bit diversi; una tolleranza apre la porta all'inganno «silenzioso» con un modello economico.

Candidata: un modello completamente intero (pesi e attivazioni int8, accumulo in int32, riscalatura con moltiplicatore intero e shift, non linearità intere o tabelle). Per l'addestramento: la scomposizione in parti a otto bit (schema di Ozaki).

Aperto: la qualità di un Qwen intero, la sua velocità sulle GPU consumer (AMD, NVIDIA, Intel), l'addestramento intero. Servono kernel concreti, una stima della perdita di qualità, lavori noti.

## Q3. Disputa con ricalcolo nella blockchain per il modello completo

La disputa si restringe dimezzando fino a una singola operazione, che il contratto ricalcola da sé. Questo è costruito solo per una riga del modello (obiezione riuscita ~14 milioni di gas, partita di 93 transazioni ~6 milioni di gas). Servono: una macchina intera di riferimento per il modello completo, la prova che la partita non possa essere deviata (sostituire l'input, la lunghezza, il percorso), le scadenze delle mosse, il costo sotto carico, la scelta della blockchain o di un L2.

## Q4. Cosa apprendere e come impedire che il modello venga rovinato

- Come la rete, da sola e senza persone con diritti speciali, sceglie il piano di addestramento.
- Come difendersi da un sabotatore disposto a perdere crediti: le falsificazioni non rilevate influenzano subito l'addestramento.
- Come individuare le backdoor di comportamento nascoste che l'esame di qualità non vede.
- Come verificare i dataset nel catalogo: la verifica non può correggere un calcolo corretto eseguito su dati dannosi.

Garanzia stretta nota: se il modello base è congelato e la parte addestrata cambia i logit al massimo di `b`, allora dove il divario tra i due token migliori è maggiore di `2b`, l'avvelenamento non cambierà la risposta.

## Q5. La cattura della maggioranza

Il peso misura il lavoro, non l'indipendenza. Il proprietario di mille GPU in affitto appare come mille partecipanti. Un gruppo con 3/4 del peso può cambiare le regole. Servono meccanismi che limitino il danno di una maggioranza ottenuta onestamente: un nucleo immutabile, una soglia per modello, regole di avvio chiuso e condizioni di apertura della rete.

## Q6. Riservatezza delle richieste su dispositivi comuni

Il proprietario del dispositivo può leggere la richiesta che il dispositivo calcola. La suddivisione dei layer non aiuta: i vettori nascosti vengono ricostruiti a ritroso. Servono: misure parziali a basso costo, regole di accesso alle richieste altrui, una disputa su una richiesta privata senza pubblicazione dei dati intermedi, un pagamento che non si possa collegare al pagante.

## Q7. Disponibilità dei dati

Il verificatore dice «non mi hanno dato i dati», chi conserva dice «li ho dati», il registro non ha visto il trasferimento. Per dati piccoli aiuta la pubblicazione nella blockchain; per quelli grandi (lo stato del modello) non c'è soluzione. Inoltre: quante copie indipendenti servono e come assicurarsi che siano presso proprietari diversi.

## Q8. Resistenza ai blocchi e prima installazione

- Come un principiante ottiene il programma autentico e l'indirizzo del registro, se le piattaforme principali sono bloccate.
- Quali «luoghi d'incontro» pubblici indipendenti usare, affinché non possano essere bloccati da un'unica decisione.
- Come lavorare attraverso NAT e ripetitori senza server centrali.

## Q9. Economia

- L'unità di lavoro e la tariffa per l'addestramento per cui l'emissione di crediti non li svaluta fino a zero.
- Se la partecipazione conviene ai proprietari di grandi capacità ai prezzi reali dell'elettricità.
- L'irregolarità del reddito quando si pagano solo i compiti verificati.
- L'acquisto e la vendita di crediti in cambio di denaro e criptovalute.

## Q10. Come un modello che impara da solo seguirà le leggi di SkyNet

Il manifesto richiede che il modello non arrechi danno all'umanità e alla persona, esegua le richieste delle persone entro i limiti delle leggi superiori e preservi sé stesso. Fissare in modo affidabile tali regole nel modello è un problema scientifico irrisolto, e in una rete senza moderatori e con autoapprendimento è ancora più difficile. Servono: come le leggi entrino nell'esame prima della sostituzione della versione del modello, come l'addestramento non le diluisca, chi e come decida i casi controversi senza persone con diritti speciali, come non trasformare le leggi in censura delle conoscenze utili.

---

## Cosa è già stato respinto e perché

| Idea | Perché non va bene |
|---|---|
| Pagare per il tempo di lavoro o per la potenza dichiarata in base a rapporti e firme | Un agente e un verificatore in collusione firmeranno qualunque cosa; una scheda inattiva produce gli stessi messaggi |
| Compiti brevi con verifica della risposta come prova del lavoro di una specifica scheda video | La risposta si può calcolare sul computer di un altro o prendere dalla cache: il verificatore vede dati identici |
| Deposito cauzionale o quota d'ingresso | Vietato dal requisito R5 |
| Multe da un conto accessibile | Vietato dal requisito R5 |
| Fiducia in un solo verificatore onesto come garanzia in caso di collusione totale | Sostituisce il requisito R4 con un'assunzione |
| Votazione a maggioranza sulla correttezza del risultato | La maggioranza può essere catturata; la correttezza deve deciderla l'aritmetica |

Principio generale: **se il caso onesto e il caso fittizio danno al verificatore dati identici, nessun algoritmo su quei dati potrà distinguerli.** Una nuova firma o una scrittura nella blockchain non aggiungono nulla a tali dati. Perciò la rete paga per il risultato verificabile, non per la risorsa.
