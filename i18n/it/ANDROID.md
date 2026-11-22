<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# Agente di ricerca SkyNet per Android (sperimentale)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · **Italiano** · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Un'app Android che porta lo stesso [agente di ricerca](../../agent/README.md) della versione
desktop. È per chi non vuole configurare Termux: installate un file, premete Avvia.
In questa fase non sono previste ricompense.

**Stato: sperimentale.** Il 22 novembre 2026 l'app è stata controllata su un emulatore
Android 14 (x86_64) con un repository di test locale firmato con una chiave di test: si è
installata, è partita, ha controllato le firme, ha calcolato tutte le 7 unità dei compiti di
test senza errori, ha atteso mentre l'emulatore era scollegato dal caricatore, ha continuato
a lavorare in background, ha salvato un token e con esso ha raggiunto la vera API di GitHub,
e si è fermata ed è ripartita mantenendo il proprio stato. Una build solo ARM (`arm64-v8a`)
ha fatto lo stesso su quell'emulatore tramite la sua traduzione ARM. La sua parte Python
supera inoltre i test su un computer. **Non è ancora stata verificata su un telefono reale**,
su Android 7–13, in esecuzioni lunghe o contro le funzioni di risparmio batteria dei
produttori di telefoni. Eseguire l'agente in [Termux](../../agent/README.md#install) resta
l'altro modo.

## Per i partecipanti

1. Scaricate `skynet-agent.apk` dalla pagina
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Aprite il file. Android vi chiede di consentire l'installazione di app dal browser o dal
   gestore file.
3. Aprite "SkyNet Agent" e premete **Avvia**. Una notifica permanente mostra che è in
   esecuzione.

Cosa sapere:

- Funziona solo mentre il dispositivo è in carica, a meno che non spuntiate "Lavora anche a
  batteria". Il caricatore viene controllato tra una porzione di lavoro e l'altra: una
  porzione già iniziata (di solito meno di un minuto) viene completata anche se scollegate il
  dispositivo.
- Non si avvia da solo dopo il riavvio del dispositivo: aprite l'app e premete di nuovo Avvia.
- Su Android 13 e versioni successive, se rifiutate le notifiche, l'app funziona comunque;
  Android la mostra allora solo nell'elenco delle app in esecuzione.
- Per pubblicare i risultati serve un token GitHub: in GitHub aprite Impostazioni →
  Impostazioni sviluppatore → Token di accesso personale, create un token che possa scrivere
  issue di repository pubblici e incollatelo nell'app. Il token viene conservato solo
  all'interno dell'app. Senza un token i risultati restano in attesa sul dispositivo (fino a
  300, poi l'app smette di calcolare).
- Android 7.0 o successivo, un dispositivo a 64 bit, circa 40 MB.
- La modalità IA facoltativa non è disponibile nell'app.
- Per rimuoverla, disinstallate l'app; sul dispositivo non resta nient'altro.

## Come si differenzia dall'agente desktop

| | Desktop | App Android |
|---|---|---|
| Codice dell'agente | `agent/skynet_agent` | lo stesso pacchetto, incorporato nell'APK |
| Lavoro | processi separati a bassa priorità | un'unità alla volta nel processo in background dell'app |
| Limite di tempo | il processo worker viene terminato | un watchdog termina il processo in background; Android lo riavvia e il compito viene lasciato ai dispositivi più veloci |
| Aggiornamenti dell'agente | versione firmata dal repository | la stessa versione firmata, controllata dal codice incorporato nell'APK: firma, ogni file, nessun file fuori dall'elenco firmato, mai sotto la versione più alta che ha già funzionato qui. Una nuova versione ha tre tentativi per raggiungere il repository; altrimenti l'app torna al codice incorporato |
| L'app stessa | programma di avvio e programma di installazione | cambia solo con un nuovo APK |
| Pubblicazione | accesso con GitHub CLI | un token incollato nell'app |

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

La parte Python dell'app è [`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py).
Viene testata su un computer da [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py).
Python è incorporato con [Chaquopy](https://chaquo.com/chaquopy/) (licenza MIT).

## Licenza

MIT, come l'agente: [agent/LICENSE](../../agent/LICENSE).
