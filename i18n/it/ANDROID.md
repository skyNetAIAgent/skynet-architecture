<!-- translation of android/README.md, source sha256: e6e5eb4a3358a14712c3c5b2e0efee2cd483b0009e7378ef16b31cc789c0d054 -->

# Agente di ricerca SkyNet per Android (sperimentale)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · [Deutsch](../de/ANDROID.md) · **Italiano** · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Un'app Android che porta gli stessi [kernel di calcolo Go](../../agent-go/README.md) della
versione desktop. Installate un file e premete Avvia. Per impostazione predefinita l'agente
firma ogni risultato sul dispositivo e lo pubblica senza un account o un token.
In questa fase non sono previste ricompense.

**Sperimentale.** La shell 0.3.0 include l'agente Go 1.0.0 (rilascio 7 del motore) nell'APK.
L'installazione sopra la 0.2.0, il ciclo di vita del servizio e il riavvio devono ancora
essere verificati su Android.

## Per i partecipanti

1. Scaricate `skynet-agent.apk` dalla pagina
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Aprite il file. Android vi chiede di consentire l'installazione di app dal browser o dal
   gestore file.
3. Aprite "SkyNet Agent" e premete **Avvia**. Una notifica permanente mostra che è in
   esecuzione.

- Funziona solo mentre il dispositivo è in carica, a meno che non spuntiate "Lavora anche a
  batteria". Scollegare il caricatore annulla l'unità corrente e la lascia disponibile per
  un'esecuzione successiva.
- Per riprendere dopo aver riavviato il dispositivo, attivate **Avvio dopo il riavvio**.
  L'opzione è disattivata per impostazione predefinita. Se premete **Arresta**, l'agente resta
  fermo anche dopo un riavvio.
- Su Android 13 e versioni successive, se rifiutate le notifiche, l'app funziona comunque;
  Android la mostra allora solo nell'elenco delle app in esecuzione.
- Se un profilo esistente usa `submit_via=github`, i suoi risultati restano in coda. Questa
  versione supporta la pubblicazione tramite record di rete firmati.
- Android 7.0 o successivo su arm64-v8a o x86_64.
- La modalità IA facoltativa non è disponibile nell'app.
- Per rimuoverla, disinstallate l'app; sul dispositivo non resta nient'altro.

## Aggiornamento dell'app

Installate la 0.3.0 sopra l'app esistente con la stessa firma del pacchetto per mantenere
l'identità del dispositivo, le impostazioni, i progressi e i risultati in coda. Dalla 0.2.0
in poi, aprendo la schermata viene controllata la presenza di un nuovo APK. Android pianifica
anche un controllo giornaliero quando è disponibile una rete, anche se l'agente è fermo. Le
restrizioni sulla batteria possono ritardare quel controllo.

L'app verifica il manifest di rilascio firmato con la chiave incorporata nell'APK. Per una
versione compatibile più recente, scarica il file di rilascio nella cache privata e ne
controlla le dimensioni e lo SHA-256. Toccate il pulsante di aggiornamento o la notifica per
installarla. Su Android 8 e versioni successive, consentite l'installazione da SkyNet Agent se
vi viene chiesto, tornate all'app e confermate nel programma di installazione di Android. Con
le notifiche disattivate, usate il pulsante nella schermata principale.

## Agente e aggiornamenti

Il servizio in primo piano avvia l'eseguibile estratto nella directory delle librerie native.
Esegue un solo worker a bassa priorità alla volta e mantiene un wake lock durante il calcolo.
Un worker che supera il limite di tempo viene arrestato e l'agente salta temporaneamente quel
compito. I nuovi compiti arrivano tramite l'indice dei compiti firmato. Il nuovo codice
eseguibile arriva con un aggiornamento dell'app.

Android verifica il certificato di firma dell'APK durante l'installazione. La chiave di
rilascio separata autentica l'indice dei compiti e il manifest di download dell'APK. L'app
controlla dimensioni, SHA-256, nome del pacchetto e codice di versione dell'APK prima di
aprire il programma di installazione.

## Compilatela da soli

Su Linux, installate Go 1.27.4 con i sorgenti, Bash, GNU patch, coreutils, file e readelf
(binutils). Per compilare l'APK servono anche JDK 17, Gradle 8.7 e Android SDK 34.

```sh
cd android
gradle assembleRelease
```

Gradle richiama `./build-go.sh`. Eseguite quello script direttamente per compilare solo i due
eseguibili `app/src/main/jniLibs/<abi>/libskynet.so`. Usa `GOOS=android`,
`CGO_ENABLED=0` e PIE per entrambe le ABI. La build arm64 usa il Go standard. Per la build
x86_64 per emulatore lo script abilita il linking interno in una copia temporanea degli
strumenti di compilazione host di Go 1.27.4. Verifica l'architettura, il punto di ingresso e
l'interprete `/system/bin/linker64` prima di installare uno dei due file.

L'APK di rilascio è `app/build/outputs/apk/release/app-release-unsigned.apk`. Usate
`zipalign`, poi `apksigner sign` con la stessa chiave dell'APK precedente per gli
aggiornamenti sul posto. Generate e firmate `android/latest.json` dall'APK firmato finale con
`tools/make_apk_manifest.py`.

## Licenza

MIT, come l'agente: [agent/LICENSE](../../agent/LICENSE).
