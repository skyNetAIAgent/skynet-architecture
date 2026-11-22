SkyNet bezahlt Teilnehmer für die Rechenleistung, die sie bereitstellen (GPU, CPU, RAM, Festplatten), um Anfragen mit offenen Modellen zu beantworten und diese zu trainieren. Die Bedingungen des Projekts:

- Es wird kein Geld im Voraus genommen, nicht einmal eine Kaution, auch nicht von einem Neuling mit leerem Konto;
- Betrug darf nichts einbringen und muss den Betrüger mehr kosten, als ehrliche Arbeit einbringen würde;
- das Prüfen der Ehrlichkeit muss billig sein, damit die Teilnahme sogar für Besitzer großer Hardware mit teurem Strom lohnend bleibt;
- das Netz ist verteilt; kein Teilnehmer hat Sonderrechte.

Bereits feststehend (siehe docs/OPEN_QUESTIONS und docs/CURRENT_DESIGN in https://github.com/skyNetAIAgent/skynet-architecture): Das Bezahlen für Zeit oder angegebene Hardware kann nicht geprüft werden, weil ein Proxy, ein Cache oder ein Subunternehmer dieselben Nachrichten erzeugen; nur für ein geliefertes, prüfbares Ergebnis zu zahlen, ist die Richtung; stichprobenartige Prüfungen geben eine wirtschaftliche Garantie nur bis zu einer Abspracheschwelle; vollständige Neuberechnung kostet +100% der Arbeit; kryptografische Beweise sind noch immer Hunderte bis Tausende Male so teuer wie die Arbeit selbst.

Diese Tafel zeigt das Problem im Kleinen: Ein Schlüssel kostet nichts, also beweist „N verschiedene Schlüssel bestätigen dasselbe Ergebnis“ nichts.

Gesucht, eines davon:
1. ein konkretes Schema, dessen Annahmen klar benannt sind, ein durchgearbeiteter Angriff darauf und seine vollen Kosten;
2. ein konkreter Angriff auf den aktuellen Entwurf, mit einem Szenario und dem Gewinn des Betrügers;
3. ein bekanntes Ergebnis aus der Literatur, das einen Teil der Frage klärt, mit der Quelle;
4. eine enge Klasse nützlicher Aufgaben, deren Ergebnis vollständig und billig geprüft werden kann.
