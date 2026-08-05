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
  categoria troppo ampia.
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

- **18 cambi di tier** (required ↔ optional) e **13 rimozioni** di tool non pertinenti
  (EEG ed ECG da SM, emicrania, AD e Parkinson; echo e monitoraggio cardiaco dall'epilessia
  temporale; imaging avanzato dalla NPH).
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
- Le vostre **descrizioni condizione-specifiche** vengono recepite, ma con un accorgimento:
  non possono comparire nella descrizione del tool che l'agente legge, perché rivelerebbero
  la diagnosi che deve invece inferire (se il tool dice "per la SM, RM encefalo e midollo con
  protocollo SM", l'agente sa già che si tratta di SM). Le inseriamo quindi nel *ground
  truth* e nella griglia di valutazione: è la sede corretta, ed è anche più utile, perché
  rende misurabile la scelta del singolo esame invece di lasciarla al giudizio.

## 5. Miastenia gravis

Le cinque annotazioni che avete inserito sotto "Peripheral neuropathy" riguardano in realtà
la miastenia gravis (anti-AChR/anti-MuSK, SFEMG, imaging del mediastino, Evoli 2019 e
Jacob 2025). Le abbiamo spostate sotto **Myasthenia gravis**, che altrimenti sarebbe rimasta
l'unica condizione senza review. Se non era intenzionale, fatecelo sapere e le rimettiamo
dove erano.

## 6. Prossimi passi

Per le quattro nuove patologie prepariamo noi una prima versione dei pannelli
(tier + descrizioni) a partire dalle linee guida che avete citato, e la troverete nella
piattaforma insieme ai casi: così la conferma è parte della review dei casi e non un compito
aggiuntivo.

Stiamo inoltre chiudendo un arretrato di difetti tecnici già noti su una parte dei casi
(riferimenti a un tool non più esistente, parametri fuori vocabolario): non avrebbe senso
farvi trovare bug che abbiamo già in lista.

Vi scriviamo appena i casi sono pronti per la review. Grazie ancora — il livello di
dettaglio dei vostri commenti sta cambiando il progetto in meglio.

A presto,
Andrea
