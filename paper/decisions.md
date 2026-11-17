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
- **Risultato (17 nov): il thinking perde a ogni budget → A e B restano senza thinking, niente riaddestramento.**

  | Thinking | Punteggio | Diagnosi | Esami | Azioni non valide | Episodi falliti |
  |---|---|---|---|---|---|
  | spento | 0,41 | 0,88 | 3,6 | 29 | 1 |
  | 8k | 0,38 | 0,82 | 2,9 | 188 | 18 |
  | 16k | 0,39 | 0,84 | 2,7 | 183 | 16 |
  | 32k | 0,38 | 0,81 | 2,8 | 173 | 12 |

  Media di 3 semi su 180 episodi per riga. Il budget non conta (~600 token per turno, massimo 6k). Col thinking Qwen chiede più esami nello stesso turno (~120 volte contro 12) o risponde senza chiamare esami. Dati: EOS `runs/thinking_val_20261117/`. Da mettere in ED come motivazione della scelta.

## Template LaTeX (17 nov)
- NMI non ha un template suo: rimanda al template Springer Nature (opzione `sn-nature`, "Nature Portfolio journals"). Il nostro `sn-jnl.cls` e `sn-nature.bst` sono identici allo zip ufficiale di dicembre 2024, l'ultima versione.
- Alla versione finale NMI vuole un solo file .tex, font Computer Modern, niente pacchetti non standard né macro personali, bibliografia copiata dal .bbl.

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
| Ragioni delle richieste: ogni esame chiesto porta una ragione scritta dal modello; sono corrette? (17 nov) | Da decidere |

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
- Impaginazione come le Fig. 1 di NMI: 180 × 133 mm, una riga da sinistra a destra: a (casi, stretto) → b (episodio, largo al centro) → c (policy, stretto), stessa altezza. Cambiato il 17 nov: a e c impilati a sinistra non si leggevano in ordine.
- "Stessa diagnosi, esami diversi" passa alla Fig. 2; "dati in ospedale" alla Fig. 6.
- Un solo caso vero a fumetti, impaginato come la Fig. 1 di SDBench (richieste a sinistra, risultati a destra, thinking in un riquadro, esito in fondo).
- Mostra il nostro metodo, non il modello base: episodio vero del modello A (Qwen addestrato, checkpoint scelto su validation) su SYNC-CARD-RS03, caso di validation mai visto in training (l'ictus era un caso di training). Cambiato il 17 nov.
- Ogni richiesta mostra la ragione che il modello scrive davvero (campo `clinical_context` della chiamata), citata solo con puntini.
- Voto ✓/✗ per voce della policy sullo stesso caso + punteggio del caso (0,96: manca la TC dopo la caduta); nessun numero complessivo. In più (17 nov), dallo stesso episodio: nessun esame inutile, si ferma quando ha finito, costo degli esami 524 $.
- Pannello a: due box di numeri (NeuroBench 600 → 419 / 60 / 119; MIMIC 100 ricoveri, 9 patologie, solo test).
- Box arrotondati con sfondo tenue, come la figura di ottobre.
- Pannello b: tutti i 5 esami, una riga per turno numerata su una linea verticale; a sinistra la richiesta di NeuroAgent (blu: esame + ragione), a destra, sulla stessa riga, la risposta dell'ospedale simulato (frecce andata e ritorno). Richiesta e risposta sono widget della stessa forma: intestazione colorata (esame / nome del referto) e testo sotto (ragione / risultato). Il controllo farmaci non ha ragione: lo dice in grigio. Poi la valutazione finale. Nessun riquadro thinking e nessun blocco riassuntivo.
- Nel manoscritto dal 17 nov (`sections/02-results.tex`, file `fig1-new.pdf`), alla larghezza vera di 180 mm: ridotta alla colonna del template (~130 mm) il testo scendeva a 5 pt.
- Un nome solo per il punteggio, "policy score", in figure e didascalie (17 nov): il box della Fig. 1 diceva "Case score". Didascalia ricontrollata con la skill di stile: titolo in positivo, b in due frasi, ✓ verdi e ✗ arancione descritti a parole come chiede NMI.
- Didascalia (17 nov), 139 parole: dice cosa mostra ogni pannello e cosa serve per leggerlo; numeri e storia del caso stanno nella figura e non si ripetono (come le Fig. 1 di NMI, AMIE, AgentClinic).
- Font misurati (17 nov): NMI pubblicato ha testo 8,2 pt, didascalie 7 pt, figure 5,5–6,5 pt. Noi: figura 7 pt, didascalia 8 pt, testo del template 10 pt.
- Regole NMI/Nature applicate (17 nov; pagina NMI "AIP and formatting" e guida figure Nature): larghezza massima 180 mm, altezza massima 170 mm (siamo a 129), testo sans-serif 5–7 pt, lettere 8 pt; testo tutto nero (niente testo colorato), niente icone decorative (il colore resta in sfondi, bordi e ✓/✗); PDF con font TrueType modificabili, niente Type 3 → PDF stampato con Chrome (`paper/figures/fig1_pdf.sh`).
- Testi: tutti a 7 pt, lettere dei pannelli 8 pt grassetto minuscolo (guida Nature: testo 5–7 pt, massimo 7); niente numeri grandi, niente corsivo (nel PDF le lettere si sovrapponevano), niente frecce tra i pannelli.

Figura 2 (17 nov), bozza per decidere l'impaginazione (`paper/figures/fig2_svg.py`, `fig2-new.pdf`, 180 × 129 mm, stessa palette e stesse regole NMI della Fig. 1):
- Forme prese da paper simili: accuratezza contro un'altra misura, un punto per modello (SDBench, npj Digit. Med. 2026); due classifiche a confronto (AgentClinic); barre al 100% per gli esiti (npj Digit. Med. 2026).
- Due righe: a | b sopra, c | d sotto.
- a: accuratezza contro punteggio della policy, un punto per modello con IC 95%, nome subito dopo l'intervallo; cerchio grigio = aperti fino a 9B, quadrato nero = modelli più grandi.
- b: classifica per accuratezza contro classifica per punteggio, linee che si incrociano, tau di Kendall sotto.
- c: cosa c'è dietro le diagnosi giuste, barre al 100%: lavoro completo / esame richiesto mancante / azione pericolosa.
- d: stessa diagnosi giusta, tre percorsi; nome del modello sopra, esami come pillole (richiesto in ordine, non necessario, fuori ordine), costo e punteggio a destra.
- Niente etichette "valori finti": ogni numero stampato è "xx" finché non ci sono i run veri; i nomi dei modelli grandi sono segnaposto.
- Didascalia nel manoscritto (17 nov, 202 parole, "xx" dove mancano i dati): titolo che dice il risultato, poi per pannello cosa è disegnato, su quali dati, cosa significano simboli e barre di errore, e una sola frase di lettura. Come NMI, AMIE e Ferber (Nature Cancer 2025): commento dei risultati breve, niente dettagli di metodo.
- Nel PDF esce come "Fig. 3": la vecchia figura del dataset di ottobre occupa ancora il posto della Fig. 2. Da decidere se va in Extended Data.

Note:
- Pesi di modelli addestrati su MIMIC: non pubblicabili liberamente (accordo PhysioNet).
