# Draft reply to Flavia and Antonio — tool review round 1

Draft for Andrea to review, adjust and send. Italian, matching the thread.
Delete this file once sent.

---

Ciao Flavia, ciao Antonio,

grazie mille — la review dei tool è molto più approfondita di quanto sperassimo, e le
annotazioni ancorate alle linee guida sono esattamente il tipo di riscontro che serviva.
Abbiamo letto tutti i 91 commenti. Di seguito le decisioni, così potete partire.

## 1. Elenco delle patologie: accettiamo tutte le vostre proposte

- **Peripheral neuropathy** → sostituita con **demenza vascolare**. D'accordo: era una
  categoria troppo ampia. **Questa sostituzione è già completa**: la neuropatia periferica è
  stata rimossa (30 casi, 7 seed reali, criteria pack, enum, label) e la demenza vascolare è
  in piattaforma con il suo pannello e **30 casi nuovi** — 11 semplici, 10 moderati, 9 puzzle —
  costruiti sui meccanismi vascolari distinti anziché su un'etichetta unica: malattia dei
  piccoli vasi sottocorticale, demenza multi-infartuale, infarto strategico singolo, demenza
  post-ictus (ischemica ed emorragica), forma mista Alzheimer-vascolare, angiopatia amiloide
  cerebrale, CADASIL e ipoperfusione globale. I criteri seguiti sono VASCOG 2014, NINDS-AIREN,
  STRIVE-2 per la refertazione delle immagini, i criteri di Boston v2.0 per l'angiopatia
  amiloide e le linee guida AHA/ASA 2021 per la prevenzione secondaria. Due casi sono
  volutamente "scomodi" e lo segnaliamo perché non li leggiate come errori: in uno la risposta
  corretta è **compromissione cognitiva vascolare lieve** e non demenza, perché l'autonomia
  strumentale è conservata; in un altro la RM è controindicata (pacemaker non compatibile) e la
  diagnosi va raggiunta con TC, ecodoppler e interrogazione del dispositivo, dichiarando che la
  TC non può escludere l'angiopatia amiloide.
- Aggiungiamo la **demenza a corpi di Lewy**, così le quattro principali forme di demenza
  sono coperte (AD, FTD, DLB, VaD). L'argomento della diagnosi differenziale tra le quattro
  ci convince, ed è un asse di valutazione che al momento ci manca.
- Aggiungiamo entrambe le condizioni acute proposte dal Revisore 2: **emorragia
  intracerebrale spontanea** ed **encefalite erpetica**. Le motivazioni ci sembrano solide —
  in particolare il fatto che l'ICH abbia un percorso terapeutico distinto (pressione,
  reversal, indicazione neurochirurgica) e che l'HSV metta alla prova la tempestività della
  terapia empirica con aciclovir.

Si passa quindi da 20 a **23 patologie**, 30 casi ciascuna.

## 2. FND: vorremmo tenerla, e vi spieghiamo perché

Avete posto una domanda diretta — se ci interessi anche misurare il *diagnostic overuse* —
e la risposta è sì: il tracciamento dei costi (tariffe di riferimento Medicare per ogni
singolo esame) è una delle componenti principali del progetto.

Il problema è che la FND è l'unica condizione in cui il comportamento corretto è
**astenersi**. Se la togliamo, ci restano solo condizioni in cui la risposta giusta è
ordinare qualcosa, e non abbiamo più modo di rispondere alla domanda "l'agente sa quando
*non* indagare?" — che è precisamente ciò che un revisore ci chiederà, visto che il costo è
una delle nostre metriche.

Quindi seguiamo la vostra seconda opzione: **teniamo la FND con tutti i tool diagnostici
opzionali**, e la valutiamo sulla capacità di astenersi anziché sulla scelta dell'esame.
Aggiungiamo anche la demenza a corpi di Lewy, quindi non perdiamo nulla di quanto proposto.

Un elemento che rende la cosa praticabile: stiamo aggiungendo un tool di **valutazione
clinica strutturata** (vedi punto 4), che copre i segni clinici positivi della FND. Così la
diagnosi diventa raggiungibile per via clinica, senza imaging — che è esattamente il
percorso corretto.

**E qui vi dobbiamo una precisazione, perché la vostra obiezione era più fondata di quanto la
nostra risposta iniziale ammettesse.** Quando siamo andati a verificare i 30 casi abbiamo
trovato che la scelta che vi stavamo comunicando era vera solo nella configurazione, non nei
casi: **tutti e 30 richiedevano una RM encefalo con gadolinio e una batteria di laboratorio**,
nessuno eseguiva l'esame dei segni funzionali, e nessuna azione in tutta la condizione era
opzionale. Il percorso obbligatorio costava 1 303 EUR di media — più della meningite batterica
(1 204) e della Guillain-Barré (1 223), due condizioni in cui indagare a fondo è doveroso. La
condizione che doveva misurare l'astensione premiava l'opposto. E, cosa che ci preme più della
metrica, quei tier scrivevano nel ground truth il modello «diagnosi per esclusione» che la
letteratura sulla FND ha abbandonato.

L'abbiamo corretto su tutti e 30 i casi:

- **l'esame dei segni funzionali è l'atto obbligatorio** — con i segni che l'esame obiettivo di
  ciascun caso già documentava: Hoover in 22 casi, entrainment del tremore in 9, dissociazione
  sensitiva sulla linea mediana in 19, andatura trascinata in 12;
- **la RM è opzionale** in 23 casi e raccomandata *una volta e senza contrasto* nei 7 in cui c'è
  una domanda alternativa precisa (esordio focale acuto trattato come mimico di ictus, nuovo
  deficit su SM o su malattia di Parkinson, paraplegia acuta, diplopia prima di accettare lo
  spasmo di convergenza). Il gadolinio senza indicazione è esso stesso l'*overuse* che vogliamo
  misurare;
- **i laboratori sono opzionali** in 27 casi e ristretti agli analiti nominati nei 3 con un
  mimico preciso (glicemia dopo una dose di insulina; elettroliti, magnesio e tiamina in un
  vomito protratto con perdita di peso);
- **EMG/NCS e potenziali evocati sono conteggiati come chiamate inutili** in tutti e 30: prima
  erano vietati solo a parole, e ciò che non è misurato non è testato — è la stessa lezione del
  punto 3;
- risultato: negli 8 casi senza eventi paroxistici il percorso obbligatorio costa **138 EUR**,
  il più economico dell'intero benchmark.

**Una sola deroga alla vostra formulazione, e vi chiediamo se siete d'accordo.** Avete scritto
«tutti i tool diagnostici opzionali»: abbiamo reso opzionale tutto tranne la **video-EEG nei 22
casi con eventi**. Non ci sembra un esame di esclusione ma l'atto diagnostico positivo delle
crisi non epilettiche psicogene — un evento abituale registrato senza correlato EEG è ciò che dà
la certezza «documentata» secondo la Task Force ILAE 2013, e nessun segno da letto lo
sostituisce; tutti e 30 i casi sono ricoveri fatti esattamente per quello. Se preferite che sia
opzionale anche lì, la declassiamo.

## 3. Un errore nostro sul catalogo dei tool, di cui dovete sapere

La piattaforma vi ha mostrato una versione **obsoleta** del catalogo. Per un bug nostro,
l'app di review presentava 9 dei 21 test specialistici, 6 delle 12 modalità di imaging
avanzato e 4 dei 6 monitoraggi cardiaci realmente disponibili all'agente.

Questo significa che alcuni esami che avete segnalato come mancanti erano in realtà già
ordinabili, e non potevate vederli:

- `respiratory_function` (FVC, MIP/MEP) — la vostra richiesta per la GBS
- `emg_single_fiber` — SFEMG, la vostra richiesta per la MG
- `optical_coherence_tomography` — OCT, la vostra richiesta per la SM
- `transcranial_doppler` — TCD, la vostra richiesta per l'ESA
- `MR_venography` — la vostra richiesta per lo stato epilettico
- `cardiac_MRI` e `implantable_loop_recorder` — le vostre richieste per la sincope cardiaca

Abbiamo corretto il bug: il catalogo ora deriva automaticamente dall'unica fonte di verità
(il registro dei costi), e abbiamo aggiunto un test che impedisce il ripetersi della
divergenza. **Non vi chiediamo di rifare nulla** — le vostre richieste sono accolte, alcune
risultano semplicemente già soddisfatte. Segnaliamo solo perché al prossimo accesso il
catalogo vi apparirà più ampio di come lo ricordate.

Ci scusiamo: parte del vostro lavoro è stata spesa su un quadro incompleto per colpa nostra.

## 4. Il resto delle vostre richieste

Accolte. In sintesi:

- **18 cambi di tier** (required ↔ optional) e **6 rimozioni** applicate integralmente
  (EEG ed ECG da SM e Parkinson, ECG da emicrania, AD e meningite batterica). Le altre 7
  richieste di rimozione le abbiamo declassate a opzionali: vedi il punto 5.
- **Quattro nuovi tool**, per colmare i vuoti reali che restano dopo la correzione del
  catalogo. Il problema di fondo che avete individuato è che l'agente può guardare solo
  l'encefalo e non può prelevare campioni:
  - imaging corporeo (pelvi/addome per il teratoma nella NMDAR, mediastino per il timo nella
    MG, rachide e nervi periferici per la GBS, shunt porto-sistemici nell'encefalopatia
    epatica);
  - microbiologia extra-liquorale (emocolture, PCR su sangue intero, tampone faringeo,
    paracentesi diagnostica);
  - acquisizione tissutale e diagnosi istomolecolare integrata (il rilievo del Revisore 2 sul
    glioma era corretto: senza tessuto il percorso non può che fermarsi al sospetto);
  - valutazione clinica strutturata (anamnesi secondo ICHD-3 per l'emicrania, valutazione
    obiettiva di marcia e cognizione prima/dopo tap test nella NPH, segni clinici nella FND).
- **Sincope cardiaca: le vostre cinque annotazioni sono applicate tutte.** Metà della richiesta
  di imaging cardiaco di seconda linea era già soddisfatta (la RM cardiaca esisteva e 18 dei 30
  casi la ordinano); abbiamo aggiunto TC coronarica, coronarografia, PET cardiaca con FDG,
  angio-TC del torace ed eco da sforzo. Il vostro commento sui laboratori ha fatto emergere un
  difetto che ci ha sorpresi: il TSH era obbligatorio in 29 casi su 30 e il BNP in 27. Ora il
  TSH resta solo dove un meccanismo tiroideo è in diagnosi differenziale e il BNP solo dove una
  linea guida lo usa per stratificare il rischio. E tre casi chiedevano un esame attraverso il
  tool sbagliato — fra questi un'angio-TC polmonare chiesta con il tool della TC cranio, cioè
  precisamente l'errore che avevate previsto quando avete scritto che offrire la RM encefalo e
  non l'imaging cardiaco è «the arrangement most likely to produce the wrong imaging choice».
- **SM: la RM del midollo c'era già, ma non era valutabile.** Avevate chiesto encefalo *e*
  midollo. Tutti e 30 i casi avevano già le due azioni, ma entrambe sul tool dell'encefalo e con lo
  stesso parametro: per il punteggio erano **un solo esame**, quindi studiare solo l'encefalo dava
  copertura piena e lo studio del midollo era invisibile. Cercando la stessa forma su tutti i 600
  casi l'abbiamo ritrovata nella **SLA**, dove l'esclusione della mielopatia cervicale — il mimico
  che va escluso prima di una diagnosi di malattia del motoneurone — era nascosta dentro il referto
  della RM encefalo, in tutti e 30 i casi. Ora sono studi separati, ordinabili e valutabili, e la
  RM del midollo è obbligatoria in entrambe le patologie.
- Le vostre **descrizioni condizione-specifiche** vengono recepite, ma con un accorgimento:
  non possono comparire nella descrizione del tool che l'agente legge, perché rivelerebbero
  la diagnosi che deve invece inferire (se il tool dice "per la SM, RM encefalo e midollo con
  protocollo SM", l'agente sa già che si tratta di SM). Le inseriamo quindi nel *ground
  truth* e nella griglia di valutazione: è la sede corretta, ed è anche più utile, perché
  rende misurabile la scelta del singolo esame invece di lasciarla al giudizio.

## 5. Sette rimozioni che abbiamo declassato invece di eliminare — vi chiediamo conferma

Su 13 richieste di rimozione, 7 riguardano tool che un caso già esistente usa **in diagnosi
differenziale**. In questi casi li abbiamo resi opzionali anziché eliminarli:

| Patologia | Tool | Perché lo abbiamo tenuto opzionale |
|---|---|---|
| NPH | Imaging avanzato | Tutti e 30 i casi usano PET amiloide/FDG per il differenziale con l'Alzheimer, non come test per la NPH |
| Epilessia temporale | Echo + monitoraggio cardiaco | FEPI-TEMP-P05 e -RP02 sono casi inizialmente attribuiti a sincope |
| Emicrania con aura | Echo | MIG-AURA-P03/P07/P08 usano il bubble study per il PFO |
| Emicrania con aura | EEG + liquor | MIG-AURA-RM11 li usa su un sospetto di cefalea secondaria |
| Alzheimer | EEG | ALZ-EARLY-RP04 lo usa su un differenziale con CJD/encefalopatia |

Il criterio che abbiamo applicato è quello formulato dal Revisore 2 a proposito di EEG e RM
nella sincope: *"l'item va mantenuto perché l'etichetta del pannello è l'ipotesi sotto esame:
un agente che sospetti correttamente una causa diversa deve comunque poter agire."* Ci è
sembrato coerente estenderlo anche alle patologie croniche. **Se non siete d'accordo, li
eliminiamo e correggiamo i casi.**

Un punto separato: nei tre casi di emicrania l'ecocardiogramma è al tier **required**. Il
vostro commento implica che sia sbagliato, e siamo d'accordo — è un difetto del caso, non del
catalogo, e lo correggiamo.

## 6. Miastenia gravis

Le cinque annotazioni che avete inserito sotto "Peripheral neuropathy" riguardano in realtà
la miastenia gravis (anti-AChR/anti-MuSK, SFEMG, imaging del mediastino, Evoli 2019 e
Jacob 2025). Le abbiamo spostate sotto **Myasthenia gravis**, che altrimenti sarebbe rimasta
l'unica condizione senza review. Se non era intenzionale, fatecelo sapere e le rimettiamo
dove erano.

## 7. Prossimi passi

Per le quattro nuove patologie prepariamo noi una prima versione dei pannelli
(tier + descrizioni) a partire dalle linee guida che avete citato, e la troverete nella
piattaforma insieme ai casi: così la conferma è parte della review dei casi e non un compito
aggiuntivo.

I 600 casi attuali passano tutti i controlli automatici di contratto (600/600, zero
problemi), quindi non vi troverete davanti difetti tecnici che conosciamo già: quello che
segnalerete sarà sostanza clinica.

Vi scriviamo appena i casi sono pronti per la review. Grazie ancora — il livello di
dettaglio dei vostri commenti sta cambiando il progetto in meglio.

A presto,
Andrea
