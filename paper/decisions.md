# Paper: decisioni

Aggiornato il 17 nov 2026. Una riga per decisione, con data.

## Rivista
- **Nature Machine Intelligence** (17 nov). ICML scartato: metodo giudicato troppo debole da solo.

## Contenuti
- Due modelli addestrati a confronto (17 nov):
  - A: premiato per gli esami giusti nell'ordine giusto (reward finale);
  - B: premiato solo per diagnosi giusta e costo basso.
- Le versioni del reward scartate, con motivo e numeri (17 nov):
  - 3 nov: rispondere senza esami prendeva ≥ di un lavoro completo in 225/600 casi → corretto;
  - 13 nov: A ordinava 5,8 esami inutili per caso → −0,03 per ogni esame inutile.

## Ragionamento dell'agente (17 nov)
- Oggi Qwen e Gemma girano col thinking spento (deciso con vLLM 0.23 e 4.096 token: Qwen finiva i token senza chiamare esami).
- Da verificare se è ancora la scelta migliore: "non renderlo più stupido del necessario".
- Prova: Qwen3.5-9B non addestrato, thinking spento vs acceso a 8k / 16k / 32k token, 60 casi di validation × 3 semi. Nessun caso di test.
- Se il thinking vince: si decide dopo aver visto quanto vince e quanto costa riaddestrare A e B.

## Validazione medica
- Stato (meeting 16 nov): ogni caso rivisto da due medici, in modo indipendente, uno dopo l'altro, sullo stesso account.
- Da chiedere / chiesto:
  - [ ] una patologia rifatta con due account diversi → accordo tra medici (kappa);
  - [ ] dopo le correzioni: campione di casi ricontrollato;
  - [ ] 20–30 casi risolti dai medici → confronto medico vs agente;
  - [ ] ~100 percorsi dei modelli giudicati alla cieca → il nostro punteggio concorda coi medici?
- Nei Metodi: ruolo ed esperienza dei medici, non i nomi.

## Dove va cosa (17 nov)
NMI: **Main** max 6 figure/tabelle e ~3.500 parole · **Extended Data (ED)** max 10, dentro l'articolo · **Supplementary** senza limite, PDF a parte.

| Esperimento | Dove |
|---|---|
| A vs B vs base, test sintetico, 3 semi | Main |
| Storia del reward (versioni scartate) | Main breve + ED |
| Modelli base: diagnosi giusta con esami sbagliati o mancanti (Qwen, Gemma, Granite, 2–3 grandi) | Main |
| Medici giudicano ~100 percorsi alla cieca: il punteggio concorda? | Main |
| Medici risolvono 20–30 casi: medico vs agente | Main |
| Trasferimento su 100 casi MIMIC neuro | Main |
| A (9B) vs modelli più grandi + costo e tempi su una GPU | Main (una figura) |
| Accordo tra medici + campione ricontrollato | Main breve + ED |
| Training su altri modelli (Gemma, Qwen piccolo, forse Granite), 1 seme | ED |
| Per patologia, con lettura clinica | ED + Discussion |
| Acute vs croniche (solo sintetico) | ED |
| Baseline senza esami e senza menu | ED |
| Agenti finti (perfetto, ordina tutto, nessun esame) | ED |
| Robustezza: pesi del punteggio cambiati | ED |
| Robustezza: casi con fatti contraddittori | ED |
| MIMIC non neurologico, sottoinsieme ~100 casi | Prova; dove va lo decidiamo dai risultati |
| RL con casi MIMIC: 50 nel training, 50 nel test (coi 100 attuali) | Esplorativo; dove va lo decidiamo dai risultati |

Figure del Main (17 nov; più esperimenti possono stare nella stessa figura, in pannelli diversi):

| Fig. | Contenuto |
|---|---|
| 1 | Panoramica: casi, esami, punteggio, revisione dei medici (+ accordo tra medici) |
| 2 | Diagnosi giusta con esami sbagliati o mancanti, modelli non addestrati |
| 3 | A vs B vs base, con la storia del reward in breve |
| 4 | I medici: (a) giudizio alla cieca vs punteggio, (b) medico vs agente sugli stessi casi |
| 5 | Casi veri MIMIC neuro |
| 6 | A vs modelli più grandi, e costo su una GPU |

Palette (17 nov), uguale in tutte le figure — Okabe-Ito, sicura per daltonici (Wong, Nat Methods 2011):

| Ruolo | Colore |
|---|---|
| Modello A (premiato sul percorso) | blu `#0072B2` |
| Modello B (premiato su diagnosi + costo) | arancio `#E69F00` |
| Base (non addestrato) | grigio `#999999` |
| Medici / policy | rosa `#CC79A7` |
| Corretto ✓ | verde `#009E73` |
| Errore ✗ | vermiglio `#D55E00` |

Figura 1 (17 nov):
- Da zero, più semplice della versione del 26 ott; file SVG, poi PDF.
- 3 pannelli in una riga, da sinistra a destra: (a) dati, (b) agente al lavoro, (c) policy dei medici.
- "Stessa diagnosi, esami diversi" passa alla Fig. 2; "dati in ospedale" alla Fig. 6.
- Un solo caso vero a fumetti, come Hager (Nat Med 2024) e SDBench: ictus ISCH-STR-S01, episodio vero di Qwen base.
- Voto ✓/✗ per voce della policy sullo stesso caso + punteggio del caso (0,54); nessun numero complessivo.
- Pannello a: due box di numeri (NeuroBench 600 → 419 / 60 / 119; MIMIC 100 ricoveri, 9 patologie, solo test).
- Box arrotondati con sfondo tenue, come la figura di ottobre.
- Pannello b con il ragionamento dell'agente (thinking) prima di ogni chiamata. Le frasi di thinking ora sono **illustrative**: vanno sostituite con una traccia vera quando finisce la prova thinking acceso/spento.

Note:
- Pesi di modelli addestrati su MIMIC: non pubblicabili liberamente (accordo PhysioNet).
