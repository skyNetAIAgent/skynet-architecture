<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# Agente di ricerca SkyNet per Android (sperimentale)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · **Italiano** · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Un'app Android che porta lo stesso [agente di ricerca](../../agent/README.md) della versione
desktop. Installate un file e premete Avvia. Per impostazione predefinita l'agente firma ogni
risultato sul dispositivo e lo pubblica senza un account o un token.
In questa fase non sono previste ricompense.

**Sperimentale.** Il 22 novembre 2026 la shell precedente è stata provata su un emulatore
Android 14. Ha completato tutte e sette le unità di test, ha atteso la ricarica e ha mantenuto
il proprio stato tra arresti e avvii. La shell 0.2.0 include l'agente 0.2.2. I suoi flussi di
installazione e riavvio devono ancora essere verificati su Android.

## Per i partecipanti

1. Scaricate `skynet-agent.apk` dalla pagina
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Aprite il file. Android vi chiede di consentire l'installazione di app dal browser o dal
   gestore file.
3. Aprite "SkyNet Agent" e premete **Avvia**. Una notifica permanente mostra che è in
   esecuzione.

- Funziona solo mentre il dispositivo è in carica, a meno che non spuntiate "Lavora anche a
  batteria". Il caricatore viene controllato tra una porzione di lavoro e l'altra: una
  porzione già iniziata (di solito meno di un minuto) viene completata anche se scollegate il
  dispositivo.
- Per riprendere dopo aver riavviato il dispositivo, attivate **Avvio dopo il riavvio**.
  L'opzione è disattivata per impostazione predefinita. Se premete **Arresta**, l'agente resta
  fermo anche dopo un riavvio.
- Su Android 13 e versioni successive, se rifiutate le notifiche, l'app funziona comunque;
  Android la mostra allora solo nell'elenco delle app in esecuzione.
- Gli utenti avanzati che selezionano `submit_via=github` possono inserire un token GitHub
  nella schermata principale.
- Android 7.0 o successivo, un dispositivo a 64 bit, circa 40 MB.
- La modalità IA facoltativa non è disponibile nell'app.
- Per rimuoverla, disinstallate l'app; sul dispositivo non resta nient'altro.

## Aggiornamento dell'app

Se avete la versione 0.1.0, installate la 0.2.0 da Releases sopra l'app esistente per
mantenere le impostazioni e i risultati in coda. Dalla 0.2.0 in poi, aprendo la schermata
viene controllata la presenza di un nuovo APK. Android pianifica anche un controllo
giornaliero quando è disponibile una rete, anche se l'agente è fermo. Le restrizioni sulla
batteria possono ritardare quel controllo.

L'app verifica il manifest di rilascio firmato con la chiave incorporata nell'APK. Per una
versione compatibile più recente, scarica il file di rilascio nella cache privata e ne
controlla le dimensioni e lo SHA-256. Toccate il pulsante di aggiornamento o la notifica per
installare l'aggiornamento. Su Android 8 e versioni successive, consentite l'installazione da
SkyNet Agent se vi viene chiesto, tornate all'app e confermate nel programma di installazione
di Android. Con le notifiche disattivate, usate il pulsante nella schermata principale.

## Come si differenzia dall'agente desktop

| | Desktop | App Android |
|---|---|---|
| Codice dell'agente | `agent/skynet_agent` | lo stesso pacchetto, incorporato nell'APK |
| Lavoro | processi separati a bassa priorità | un'unità alla volta nel processo in background dell'app |
| Limite di tempo | il processo worker viene terminato | un watchdog termina il processo in background; Android lo riavvia e il compito viene lasciato ai dispositivi più veloci |
| Aggiornamenti dell'agente | versione firmata dal repository | l'APK verifica i file firmati e il numero di rilascio. Un nuovo agente ha tre avvii per superare un autocontrollo locale e completare un passo del ciclo |
| L'app stessa | programma di avvio e programma di installazione | un APK verificato installato con la vostra conferma |
| Pubblicazione | record firmati per impostazione predefinita | record firmati per impostazione predefinita |

Limiti, onestamente. L'APK è firmato con una chiave detenuta dai manutentori del progetto; Android
accetta un aggiornamento dell'app solo se è firmato con la stessa chiave. La chiave di rilascio
(per il codice dell'agente e gli elenchi dei compiti) e questa chiave dell'APK sono due singoli
punti di fiducia che la rete SkyNet finale non deve avere. L'app carica codice Python firmato
in fase di esecuzione, cosa che le regole di Google Play non consentono, quindi è distribuita
come file.

## Compilatela da soli

Servono JDK 17, l'Android SDK (platform 34, build-tools 34), Gradle 8.7 e Python 3.12 sul
computer di compilazione.

```sh
cd android
gradle assembleRelease
```

Il risultato è `app/build/outputs/apk/release/app-release-unsigned.apk`. Firmatelo con la
vostra chiave (`zipalign`, poi `apksigner sign`) prima di installarlo. Un APK firmato da voi
non può essere installato sopra quello del progetto, e viceversa.

Compilate l'app solo da un commit in cui `agent/skynet_agent/trust.py` elenca la chiave di
rilascio: un agente senza chiave di rilascio non accetta compiti. La build di rilascio si
ferma con un errore in quel caso; `-PallowNoReleaseKey` compila comunque un APK del genere,
solo per i test.

Il bridge dell'agente e il verificatore dell'APK hanno test Python separati sul desktop.
[Test dell'agente](../../agent/tests/test_android_glue.py) · [Test degli aggiornamenti dell'APK](../../agent/tests/test_apk_update.py)
Python è incorporato con [Chaquopy](https://chaquo.com/chaquopy/) (licenza MIT).

## Licenza

MIT, come l'agente: [agent/LICENSE](../../agent/LICENSE).
