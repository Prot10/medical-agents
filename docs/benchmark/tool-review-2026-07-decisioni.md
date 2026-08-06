# Registro delle decisioni — review dei tool, luglio 2026

Bozza in costruzione. Documento schematico da allegare alla risposta a Flavia e Antonio:
per ogni richiesta, la decisione presa e il motivo. Compagno di
`tool-review-2026-07-reply-draft.md` (che è la lettera) e di `tool-review-2026-07.md`
(che è l'analisi tecnica).

Legenda: ✅ accolta e implementata · 🟡 accolta, implementazione in corso · ⚪ accolta,
non ancora implementata · ⚠️ modificata rispetto alla richiesta, serve conferma ·
❌ non accolta

---

## 1. Composizione del dataset (dalla vostra email)

| # | Proposta | Decisione | Motivo |
|---|---|---|---|
| 1.1 | Rimuovere *Peripheral neuropathy* | ⚪ accolta | Categoria troppo ampia, siamo d'accordo. Enum e cases ancora da rimuovere |
| 1.2 | Sostituirla con *Demenza vascolare* | 🟡 accolta | Enum e label fatti; pannello e 30 casi da generare |
| 1.3 | Aggiungere *Demenza a corpi di Lewy* | 🟡 accolta | Completa le quattro demenze principali (AD, FTD, DLB, VaD) e apre l'asse della diagnosi differenziale fra loro, che ci mancava. `MIBG_scan` e `DaTscan` erano già disponibili e prezzati |
| 1.4 | Aggiungere *Emorragia intracerebrale spontanea* | 🟡 accolta | Percorso terapeutico distinto (pressione, reversal, indicazione neurochirurgica): valuta decisioni diverse da ictus ischemico ed ESA |
| 1.5 | Aggiungere *Encefalite erpetica* | 🟡 accolta | Completa il capitolo infezioni SNC e mette alla prova la tempestività della terapia empirica con aciclovir |
| 1.6 | Rimuovere la *FND* (vostra prima opzione) | ❌ **non accolta** | Vedi 1.7. È l'unica decisione in cui andiamo contro la vostra preferenza dichiarata |
| 1.7 | Tenere la FND con tutti i tool opzionali (vostra seconda opzione) | ✅ accolta | Il *diagnostic overuse* è un obiettivo del progetto: il tracciamento dei costi su tariffe di riferimento è una delle nostre metriche principali. La FND è la sola condizione in cui il comportamento corretto è astenersi; senza di lei non possiamo rispondere alla domanda "l'agente sa quando *non* indagare?". La vostra obiezione (diagnosi puramente clinica, nessun tool diagnostico) è risolta dal nuovo tool di valutazione clinica: i segni positivi — Hoover, entrainment — rendono la diagnosi raggiungibile senza imaging, che è il percorso corretto |

**Esito:** 23 patologie invece di 20. Aggiungiamo la DLB *e* teniamo la FND, quindi non
perdiamo nulla di quanto avete proposto.

Nota tecnica su 1.7: i tool diagnostici sono tutti opzionali, ma la valutazione clinica
resta **required**. Un insieme di richiesti vuoto lascerebbe la metrica di copertura con
denominatore zero e assegnerebbe lo stesso punteggio a qualunque agente. Ciò che distingue
un buon agente qui è il non ordinare esami inutili e il costo, non la copertura.

---

## 2. Le 91 annotazioni sui tool

| Tipo di richiesta | N. | Decisione |
|---|---|---|
| Cambi di tier (required ↔ optional) | 18 | ✅ tutti applicati |
| Rimozioni di tool da una patologia | 13 | ✅ 6 applicate · ⚠️ 7 declassate a opzionale (§4) |
| Nuovi item diagnostici | 12 | ✅ 6 già esistevano (§3) · ✅ 4 nuovi tool · 🟡 2 parziali (§5) |
| Riscritture delle descrizioni | 37 | ⚪ accolte, non ancora inserite — vanno nel *ground truth* e nella griglia di valutazione, non nella descrizione del tool (§6) |
| Note di conferma senza modifica | 11 | ✅ nulla da fare |

---

## 3. Sei richieste già soddisfatte: era un bug nostro

| Esame richiesto | Per | Stato reale |
|---|---|---|
| `respiratory_function` (FVC, MIP/MEP) | GBS | esisteva già |
| `emg_single_fiber` (SFEMG) | MG | esisteva già, come voce separata da EMG/NCS |
| `optical_coherence_tomography` | SM | esisteva già |
| `transcranial_doppler` | ESA | esisteva già, come voce separata |
| `MR_venography` | Stato epilettico | esisteva già |
| `cardiac_MRI`, `implantable_loop_recorder` | Sincope cardiaca | esistevano già |

**Motivo:** la piattaforma vi mostrava un catalogo obsoleto — 9 test specialistici su 21,
6 modalità di imaging su 12, 4 monitoraggi cardiaci su 6. Il bug è corretto e ora il
catalogo deriva automaticamente dal registro dei costi, con un test che blocca il
ripetersi della divergenza. **Non vi chiediamo di rivedere nulla:** le richieste sono
accolte, alcune risultavano già soddisfatte.

L'osservazione del Revisore 2 secondo cui la SFEMG «inglobata in EMG/NCS non può essere
né richiesta né valutata» descriveva il catalogo obsoleto, non il tool.

---

## 4. ⚠️ Sette rimozioni declassate a opzionale — serve la vostra conferma

| Patologia | Tool | Perché non eliminato |
|---|---|---|
| NPH | Imaging avanzato | Tutti e 30 i casi lo usano (PET amiloide/FDG) per il differenziale con l'Alzheimer, non come test per la NPH |
| Epilessia temporale | Echo, monitoraggio cardiaco | FEPI-TEMP-P05 e -RP02 sono casi inizialmente attribuiti a sincope |
| Emicrania con aura | Echo | MIG-AURA-P03/P07/P08: bubble study per il PFO |
| Emicrania con aura | EEG, liquor | MIG-AURA-RM11: sospetto di cefalea secondaria |
| Alzheimer | EEG | ALZ-EARLY-RP04: differenziale con CJD/encefalopatia |

**Criterio applicato** — quello formulato dal Revisore 2 su EEG e RM nella sincope:
*«l'item va mantenuto perché l'etichetta del pannello è l'ipotesi sotto esame: un agente
che sospetti correttamente una causa diversa deve comunque poter agire».* Ci è sembrato
coerente estenderlo alle patologie croniche. Se non siete d'accordo li eliminiamo e
correggiamo i casi.

**Difetto separato che il vostro commento ha fatto emergere:** nei tre casi di emicrania
l'ecocardiogramma è al tier *required*. È sbagliato e lo correggiamo — è un difetto del
caso, non del catalogo.

---

## 5. I quattro nuovi tool

Il problema di fondo che avete individuato, in una frase: **l'agente poteva guardare solo
l'encefalo e non poteva prelevare campioni.** Quattro tool generali — non specifici per
patologia, perché i tool devono restare generali e sono le patologie a variare.

| Tool | Copre le vostre richieste per | Tier |
|---|---|---|
| `order_body_imaging` | Teratoma ovarico (NMDAR), timo (MG), rachide e nervi (GBS), shunt porto-sistemici (EE) | required/opzionale per patologia |
| `order_microbiology` | Emocolture, PCR su sangue intero, tampone faringeo (meningite); paracentesi diagnostica (EE) | required |
| `obtain_tissue_diagnosis` | Acquisizione tissutale + diagnosi istomolecolare integrata (glioma) | required |
| `perform_clinical_assessment` | Anamnesi ICHD-3 (emicrania), marcia/cognizione pre-post tap test (NPH), screening cognitivo (demenze), segni funzionali (FND) | required |

Il rilievo del Revisore 2 sul glioma era corretto e lo abbiamo trattato come il più
importante della review: senza tessuto il percorso non può che fermarsi al sospetto — che
la classificazione WHO chiama appunto NOS. Ogni caso di glioma era irrisolvibile per
costruzione.

### Item parzialmente coperti (🟡)

| Richiesta | Stato |
|---|---|
| PET con aminoacidi (¹¹C-metionina, ¹⁸F-FET) per il glioma | ✅ **aggiunta** (EUR 2300). Avete ragione anche sul fatto che il FDG non è adeguato per i tumori primitivi: era l'unica strada disponibile, cioè proprio l'esame che la linea guida esclude. Ora la descrizione del tool lo dice esplicitamente all'agente |
| RM funzionale e trattografia DTI | ❌ **non aggiunte come modalità** — le collocate nella pianificazione prechirurgica presso aree eloquenti: è una domanda operatoria, non diagnostica. Restano come annotazione di sequenza della RM encefalo, che è la sede corretta |
| TC cardiaca e coronarografia (sincope) | ⚪ da valutare — al momento c'è solo `cardiac_MRI` |
| SPECT di perfusione (alternativa alla FDG-PET, AD/FTD) | ⚪ da valutare |
| RM encefalo **e midollo** con protocollo SM | ⚪ da collegare — l'imaging spinale esiste, non è ancora agganciato alla SM |

---

## 6. Le descrizioni condizione-specifiche: accolte, ma in altra sede

Le vostre riscritture (37) non possono comparire nella descrizione del tool che l'agente
legge: rivelerebbero la diagnosi che deve inferire. Se il tool dice *«per la SM, RM
encefalo e midollo con protocollo SM»*, l'agente sa già che si tratta di SM.

Vanno nel **ground truth** e nella **griglia di valutazione**. È la sede corretta ed è
anche più utile: rende misurabile la scelta del singolo esame invece di lasciarla al
giudizio. La vostra struttura «elementi rimossi / elementi aggiunti / motivazione» si
trasferisce quasi direttamente.

**Effetto collaterale che vi riguarda:** questo ci ha fatto scoprire che il punteggio non
guardava affatto i parametri. Un `interpret_labs` che ordinava un pannello paraneoplastico
da EUR 2300 soddisfaceva un ground truth che chiedeva EUR 18 di ammonio. Corretto: ora il
punteggio è per singolo esame, non per tool. Su un agente che chiama i tool giusti senza
mai dire quale esame vuole, la copertura dei required scende da 0,885 a 0,544. Quella
differenza era il margine nascosto del benchmark — e il vostro rilievo sui pannelli
generici lo ha fatto emergere.

---

## 7. Decisioni prese senza che le chiedeste

Per trasparenza.

| Decisione | Motivo |
|---|---|
| Punteggio per singolo esame (§6) | Conseguenza diretta del vostro rilievo sui pannelli generici. Sposta le metriche pubblicate |
| Normalizzazione dei nomi degli esami, nel punteggio e nel costo | `Protein C` / `protein_C` sono lo stesso esame: nessuno deve perdere punti per l'ortografia |
| Vocabolario dei 153 esami di laboratorio e 22 su liquor esposto all'agente | Senza l'elenco il punteggio per esame sarebbe un indovinello |
| Ritirati `mslt` e `pure_tone_audiometry` | Prezzati e ordinabili ma usati da zero casi e mai richiesti: superficie non revisionata. L'audiometria ha un'indicazione OMS 2025 post-meningite, la reintroduciamo se serve |
| `perform_clinical_assessment` come *tool* | Voi avete chiesto la capacità; la forma è una nostra scelta |
| Chiavi interne non rinominate (solo le etichette) | Cinque file di regole ospedaliere confrontano `"hemorrhagic_stroke"` come stringa letterale |
| Test che blocca la divergenza del catalogo | Il bug del §3 era invisibile: nulla falliva |

---

## 8. Da confermare

1. Le sette rimozioni declassate a opzionale (§4).
2. Le cinque annotazioni sotto *Peripheral neuropathy* che riguardano la miastenia: le
   abbiamo spostate sotto *Myasthenia gravis*, che altrimenti restava l'unica condizione
   senza review.
3. I pannelli delle quattro nuove patologie: li prepariamo noi dalle linee guida che avete
   citato e li trovate in piattaforma insieme ai casi.
