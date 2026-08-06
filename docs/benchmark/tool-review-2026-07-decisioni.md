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
| 1.1 | Rimuovere *Peripheral neuropathy* | ✅ **completata** | Categoria troppo ampia, siamo d'accordo. Rimossi i 30 casi, i 7 seed reali, il criteria pack, la voce del filtro MedCaseReasoning, il valore dell'enum e la label dell'app di review |
| 1.2 | Sostituirla con *Demenza vascolare* | ✅ **completata** | Pannello in `conditions.yaml`, criteria pack `VASC-DEM.md` (VASCOG 2014 / NINDS-AIREN / STRIVE-2 / Boston v2.0 / AHA-ASA 2021), **30 casi generati** (11 S / 10 M / 9 P) su sette meccanismi vascolari, split rigenerato preservando le assegnazioni precedenti. Tutti i gate verdi: 600/600 casi puliti, agente perfetto 1.0 su 600/600 |
| 1.3 | Aggiungere *Demenza a corpi di Lewy* | 🟡 accolta | Completa le quattro demenze principali (AD, FTD, DLB, VaD) e apre l'asse della diagnosi differenziale fra loro, che ci mancava. `MIBG_scan` e `DaTscan` erano già disponibili e prezzati |
| 1.4 | Aggiungere *Emorragia intracerebrale spontanea* | 🟡 accolta | Percorso terapeutico distinto (pressione, reversal, indicazione neurochirurgica): valuta decisioni diverse da ictus ischemico ed ESA |
| 1.5 | Aggiungere *Encefalite erpetica* | 🟡 accolta | Completa il capitolo infezioni SNC e mette alla prova la tempestività della terapia empirica con aciclovir |
| 1.6 | Rimuovere la *FND* (vostra prima opzione) | ❌ **non accolta** | Vedi 1.7. È l'unica decisione in cui andiamo contro la vostra preferenza dichiarata |
| 1.7 | Tenere la FND con tutti i tool opzionali (vostra seconda opzione) | ✅ **completata nei casi** | Il *diagnostic overuse* è un obiettivo del progetto: il tracciamento dei costi su tariffe di riferimento è una delle nostre metriche principali. La FND è la sola condizione in cui il comportamento corretto è astenersi; senza di lei non possiamo rispondere alla domanda "l'agente sa quando *non* indagare?". La vostra obiezione (diagnosi puramente clinica, nessun tool diagnostico) è risolta dal nuovo tool di valutazione clinica: i segni positivi — Hoover, entrainment — rendono la diagnosi raggiungibile senza imaging, che è il percorso corretto |

**Esito:** 23 patologie invece di 20. Aggiungiamo la DLB *e* teniamo la FND, quindi non
perdiamo nulla di quanto avete proposto.

### 1.7bis — La scelta era registrata ma non implementata: ora lo è (2026-08-06)

Vale la pena dirlo per come lo abbiamo trovato, perché la vostra obiezione era più fondata di
quanto la nostra prima risposta ammettesse. Il pannello diceva già «esame clinico obbligatorio,
strumentale tutto opzionale». I 30 casi dicevano il contrario:

| | prima | ora |
|---|---|---|
| Casi che richiedevano la RM encefalo **con gadolinio** | 30 / 30 | 0 — opzionale in 23, raccomandata *una volta e senza contrasto* nei 7 con una domanda alternativa precisa |
| Casi che richiedevano una batteria di laboratorio | 30 / 30 | 0 — opzionale in 27, raccomandata e ristretta ad analiti nominati nei 3 con un mimico preciso |
| Azioni `perform_clinical_assessment` | 0 | **30 / 30, obbligatoria** — con i segni positivi che l'esame di ciascun caso già documentava (Hoover in 22, entrainment in 9, dissociazione sensitiva sulla linea mediana in 19, andatura trascinata in 12) |
| Azioni al tier `optional` in tutta la condizione | 0 | presenti in tutti i casi |
| EMG/NCS e potenziali evocati | vietati solo a parole | **conteggiati come chiamate inutili** in tutti e 30 |
| Costo del percorso obbligatorio | 1 303 EUR di media, più della meningite batterica (1 204) | **138 EUR** negli 8 casi senza eventi — il percorso corretto più economico di tutto il benchmark |

Al di là della metrica, i tier di prima scrivevano nel ground truth il modello «diagnosi per
esclusione», che la letteratura ha abbandonato: la FND si diagnostica per segni positivi.
Correggendoli non abbiamo piegato la clinica alla metrica: abbiamo tolto un errore clinico.

Nota tecnica: la valutazione clinica resta **required** e un insieme di richiesti vuoto
lascerebbe la copertura con denominatore zero, assegnando lo stesso punteggio a qualunque
agente. Ciò che distingue un buon agente qui è il non ordinare esami inutili e il costo, non la
copertura. **Una sola deroga alla vostra formulazione**, con la motivazione clinica, al punto 5
del §8: la video-EEG resta obbligatoria dove ci sono eventi da registrare.

---

## 2. Le 91 annotazioni sui tool

| Tipo di richiesta | N. | Decisione |
|---|---|---|
| Cambi di tier (required ↔ optional) | 18 | ✅ tutti applicati |
| Rimozioni di tool da una patologia | 13 | ✅ 6 applicate · ⚠️ 7 declassate a opzionale (§4) |
| Nuovi item diagnostici | 12 | ✅ 6 già esistevano (§3) · ✅ 4 nuovi tool · ✅ 2 completati (glioma, sincope: §5, §5.1) · ⚪ 2 da valutare |
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
| Imaging cardiaco di seconda linea (RM cardiaca, TC cardiaca, coronarografia) | ✅ **completato** — vedi §5.1 |
| SPECT di perfusione (alternativa alla FDG-PET, AD/FTD) | ⚪ da valutare |
| RM encefalo **e midollo** con protocollo SM | ✅ **fatto** — e non era un collegamento: vedi §5.2 |

### 5.1 Imaging cardiaco di seconda linea — la sincope cardiaca, chiusa per intero ✅

La metà della vostra richiesta era già soddisfatta: `cardiac_MRI` esisteva e **18 dei 30 casi
la ordinano già** con il parametro esplicito. Era il catalogo obsoleto a nascondervela.
L'altra metà è stata aggiunta, con la vostra stessa gerarchia di evidenza — l'escalation
TC/RM su testo consultivo, la coronarografia con la sua raccomandazione di Classe IIa:

| Aggiunto | Tool | € | Nota |
|---|---|---|---|
| `coronary_CTA` | imaging avanzato | 460 | via non invasiva all'ischemia |
| `coronary_angiography` | imaging avanzato | 2760 | il pezzo Classe IIa |
| `cardiac_FDG_PET` | imaging avanzato | 2300 | studio distinto dalla PET cerebrale: preparazione dietetica, acquisizione gated |
| `chest_CT` / `chest_CTA` | imaging corporeo | 276 / 368 | la «cardiac or thoracic CT angiography» che chiedevate |
| `exercise_echo` | ecocardiogramma | 460 | il vostro item di Classe I nella cardiomiopatia ipertrofica |
| `lymph_node_biopsy` | diagnosi tissutale | 1840 | conferma istologica per via extracardiaca |

**Tre casi modellavano un esame con il tool sbagliato, e i vostri commenti li hanno fatti
emergere:**

- **SYNC-CARD-RM04** (embolia polmonare) chiedeva un'angio-TC polmonare attraverso il tool
  della **TC cranio**, che non ha un parametro di regione. I suoi discriminanti erano identici
  a un'angio-TC cranio-cervicale: un agente che in quel paziente avesse studiato il cervello
  prendeva comunque il punto. È esattamente «the arrangement most likely to produce the wrong
  imaging choice» che avevate previsto.
- **SYNC-CARD-RP05** (sarcoidosi cardiaca) usava `FDG_PET`, la PET cerebrale, per una PET/TC
  cardiaca con preparazione dietetica; e metteva la conferma istologica come referral senza
  tool — lo stesso schema a cui obiettavate nel glioma. Ora è una biopsia linfonodale
  chiamabile e valutabile.
- **SYNC-CARD-P02** (cardiomiopatia ipertrofica) modellava l'**eco da sforzo** come test
  ergometrico. Un tapis roulant prendeva il punto di un esame il cui intero contenuto è un
  gradiente provocato *per immagine*.

**La vostra direttiva sui laboratori, applicata a tutti e 30 i casi.** Il TSH era nel pannello
obbligatorio di 29 casi su 30 e il BNP di 27 — contro un vostro commento che dice
letteralmente che i pannelli non mirati (tiroide, infiammazione, autoimmunità, paraneoplastica)
non hanno ruolo stabilito qui e che i peptidi natriuretici non stabiliscono la causa della
sincope. Ora:

- il TSH resta nei **4** casi in cui un meccanismo tiroideo è davvero in diagnosi differenziale
  (tachicardia sopraventricolare, flutter atriale, disfunzione del nodo del seno, QT lungo);
- il BNP nei **3** in cui una linea guida lo usa per stratificare il rischio del meccanismo
  già accertato (ESC 2019 per l'embolia polmonare) o in cui una decisione sul device dipende
  dalla gravità dello scompenso;
- il passo dei laboratori è `required` in **11** casi e `recommended` in **19**;
- la spesa di laboratorio imposta sui 30 casi scende da EUR 6108 a EUR 4686 (circa 47 € per
  caso), e le azioni obbligatorie da 204 a 185.

Il vostro commento ha fatto emergere anche **un vincolo di sequenza che contraddiceva la
vostra stessa direttiva**: 28 casi imponevano i laboratori *prima* del monitoraggio cardiaco a
severità `hard`. Con i laboratori non più obbligatori, un agente che correttamente salta un
pannello non mirato per andare al monitoraggio subiva una violazione. Rimosso nei 18 casi in
cui il passo non è più obbligatorio, mantenuto dove un esame nominato apre la decisione.

### 5.2 RM encefalo **e midollo** nella SM — e il midollo nascosto in 63 azioni ✅

Avevate chiesto la RM dell'encefalo **e del midollo** con protocollo SM. Vi rispondiamo che c'era
già, ma non nel senso che pensavamo: **tutti e 30 i casi di SM avevano già due azioni obbligatorie
di RM**, encefalo e midollo cervico-dorsale — solo che entrambe erano `analyze_brain_mri` con lo
stesso `protocol: ms`, e quella del midollo era marcata da un'annotazione `region` che lo schema
del tool encefalo non ha e scarta.

Conseguenza: **le due azioni avevano la stessa identità e collassavano in una**. Un agente che
studiava solo l'encefalo prendeva la copertura piena dei required per la SM, e lo studio del
midollo — che conta per la disseminazione nello spazio, e le cui lesioni corte sono ciò che separa
la SM dalla NMOSD — era invalutabile.

Cercando questa forma su tutti i 600 casi l'abbiamo trovata altre due volte:

- **Tutti e 30 i casi di SLA** portavano `include_cervical_spine: true` sulla RM encefalo, con i
  reperti cervicali scritti dentro il referto cerebrale. Quindi l'**esclusione della mielopatia
  compressiva** — il mimico che va escluso prima di una diagnosi di malattia del motoneurone — non
  era né ordinabile separatamente né valutabile. Ora sono due studi, con i reperti spinali spostati
  nel referto del rachide.
- **Altri 3 casi**: una TC torace-addome-pelvi paraneoplastica sul tool della TC cranio, e una RM
  del midollo e una del plesso lombosacrale sul tool dell'encefalo.

Nella stessa ricerca sono emerse due altre forme di collasso, entrambe reali: **9 casi di ictus**
ordinavano l'angio-RM e poi «consideravano» lo stesso esame una seconda volta (un esame, due
azioni), e **6 azioni erano attaccate a un tool che non le esegue** — un trial con benzodiazepina
letto sull'EEG in corso, la prosecuzione dell'aciclovir come controllo di interazioni, un drenaggio
lombare prolungato come seconda analisi del liquor, una biopsia osteomidollare e una consulenza
ematologica come ricerche bibliografiche. Ora sono azioni cliniche senza tool.

Due controlli automatici nuovi impediscono il ritorno di questa classe, ed entrambi i pannelli
adesso dicono quello che i casi fanno: la RM del midollo è **obbligatoria** nella SM e nella SLA.

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
| Descrizioni del catalogo riscritte dove la modifica riguarda l'esame e non la patologia | Le stringhe che avete citato come *«current description (to be removed)»* sono quelle del catalogo, e due erano proprio quelle che avevate riconosciuto come ereditate da un pannello neuroimmunologico: laboratori e liquor. Sono corrette. Al prossimo accesso il testo che vedete è cambiato — non è un errore |
| `ASO` e `AED_levels` prezzati e ordinabili | Due casi affermavano nel *ground truth* un risultato (titolo antistreptolisinico, livello dell'antiepilettico) che l'agente non poteva chiedere perché l'esame non aveva prezzo |
| Un esame condannato dentro un prelievo multiplo ora conta | «Questo singolo dosaggio non è indicato qui» era inesprimibile: il confronto era per uguaglianza esatta, quindi non scattava mai su una richiesta reale che raggruppa più analiti. Sette classificazioni del dataset erano morte, cinque su un parametro inesistente |
| Il tool della TC dichiara di essere solo cranio-cervicale | Non ha un parametro di regione, quindi una TC del torace chiesta lì è indistinguibile da un'angio-TC del collo per il punteggio |
| Normalizzazione dei nomi degli esami, nel punteggio e nel costo | `Protein C` / `protein_C` sono lo stesso esame: nessuno deve perdere punti per l'ortografia |
| Vocabolario dei 153 esami di laboratorio e 22 su liquor esposto all'agente | Senza l'elenco il punteggio per esame sarebbe un indovinello |
| Ritirati `mslt` e `pure_tone_audiometry` | Prezzati e ordinabili ma usati da zero casi e mai richiesti: superficie non revisionata. L'audiometria ha un'indicazione OMS 2025 post-meningite, la reintroduciamo se serve |
| `perform_clinical_assessment` come *tool* | Voi avete chiesto la capacità; la forma è una nostra scelta |
| Chiavi interne non rinominate (solo le etichette) | Cinque file di regole ospedaliere confrontano `"hemorrhagic_stroke"` come stringa letterale |
| Test che blocca la divergenza del catalogo | Il bug del §3 era invisibile: nulla falliva |

---

## 7bis. Quello che la sincope ha fatto emergere su tutto il dataset

La sincope era una patologia su venti, ed è l'unica che avevamo esaminato da vicino. Abbiamo
passato le sue classi di difetto su tutti i 600 casi e le abbiamo ritrovate tutte. Sono chiuse.
Nessuna faceva cadere un controllo automatico: i controlli verificano che il *ground truth* sia
legale e raggiungibile, non che nomini l'esame che intende.

| Difetto | Quanto | Cosa abbiamo fatto |
|---|---|---|
| Le emocolture erano prezzate sotto **due** tool | 123 azioni in 108 casi ordinavano emocolture, urinocoltura o paracentesi attraverso il tool dei laboratori | Tutte su `order_microbiology`. 43 referti colturali esistevano già come follow-up dei laboratori — germe, flaconi, antibiogramma — e sono stati trasferiti, non reinventati |
| Il tool della TC cranio usato per torace/addome/pelvi | 89 azioni: miastenia 30 (mediastino), NMDAR 30 (ricerca del teratoma), glioma 27 (stadiazione), stato epilettico 2 | Tutte su `order_body_imaging`. Come per la sincope: quel tool non ha un parametro di regione, quindi quelle azioni erano indistinguibili da uno studio cranio-cervicale |
| Azioni di laboratorio/liquor obbligatorie che **non nominavano alcun esame** | 246 — qualunque chiamata al tool le soddisfaceva, quindi il punteggio per singolo esame era inerte proprio dove il vostro rilievo mirava | 153 vincolate agli esami che il loro stesso testo nomina. 95 restano volutamente generiche: un liquor la cui risposta è nella conta cellulare e nelle proteine, sempre refertate, non ha una sotto-scelta da fare |
| Due nomi prezzati per lo stesso esame che non si confrontavano uguali | `syphilis` in 30 azioni contro `RPR` in 118; pannello paraneoplastico 37 contro 1 | Risolti a un nome canonico: 69 termini riscritti. `lactate` e `ABG` ora sono prezzati — oltre 100 azioni li nominavano e nessun agente poteva chiederli |
| L'etichetta aggregata obbligatoria mentre il referto atteso nomina i componenti | 31 azioni chiedevano «indici di infiammazione» mentre l'atteso nomina procalcitonina e PCR: **un agente che ordinava esattamente l'esame giusto sbagliava** | Sostituita dai componenti. Dove il caso non nomina componenti (GBS) l'etichetta aggregata è ciò che intende e resta |
| Un vincolo `hard` su un prerequisito che il caso non richiede | 8 casi — cinque subordinavano la rachicentesi a un imaging solo raccomandato, tre la scelta del farmaco a un ECG che un caso non ordinava mai | Prerequisiti portati a obbligatori, con i referti mancanti scritti. Nuovo controllo automatico che impedisce il ripetersi |

Due di queste chiudono un pezzo di lavoro che avevamo in lista come «casi da scrivere»: il passo
di microbiologia mancante in meningite ed encefalopatia epatica (60 casi) e l'imaging corporeo
mancante in miastenia e NMDAR (60) **c'erano già, sul tool sbagliato**.

**Un ultimo difetto, sul simulatore.** Un tool che sta per più studi restituiva quello che aveva
in archivio: una PET cardiaca a chi ordinava una PET cerebrale, un'emocoltura a chi chiedeva il
liquido ascitico, un tilt-table a chi chiedeva un test ergometrico. Ora controlla il discriminante.

**E quel controllo ha fatto emergere la cosa più grossa del giro.** Una volta che il simulatore
verifica *quale* esame è stato chiesto, si può fare la domanda giusta: ogni passo del percorso di
riferimento riceve davvero una risposta? **No: 194 azioni su 600 casi no.** 98 non ricevevano
nulla — 12 obbligatorie — e 96 ricevevano il referto generico «esame fuori percorso, non
contributivo» pur avendo un reperto atteso dichiarato. Prima del controllo ricevevano tutte **il
referto di un altro esame**: chi ordinava un Doppler transcranico riceveva un eco-Doppler carotideo,
chi ordinava un ice-pack test riceveva una stimolazione ripetitiva. Il validatore era soddisfatto,
perché chiedeva soltanto se quel tool avesse *un qualsiasi* referto in archivio.

Tutte e 194 ora hanno il proprio referto, scritto a partire da ciò che ogni azione già dichiarava
nel proprio reperto atteso. Nulla è inventato: il caso si era già impegnato sul risultato.

Nel farlo sono emersi anche **20 referti di RM cardiaca etichettati `perfusion_MRI`**, cioè lo studio
cerebrale — il contenuto era cardiaco (enhancement tardivo in territorio coronarico), l'etichetta no,
ed era quella che il ground truth confrontava.

---

## 8. Da confermare

1. Le sette rimozioni declassate a opzionale (§4).
2. Le cinque annotazioni sotto *Peripheral neuropathy* che riguardano la miastenia: le
   abbiamo spostate sotto *Myasthenia gravis*, che altrimenti restava l'unica condizione
   senza review.
3. I pannelli delle quattro nuove patologie: li prepariamo noi dalle linee guida che avete
   citato e li trovate in piattaforma insieme ai casi.
4. Due tier di pannello che i casi contraddicono in modo sistematico, e che secondo noi sono i
   pannelli a sbagliare: la **TC cranio** è opzionale nella meningite batterica e
   nell'encefalopatia epatica, ma 27 e 30 casi rispettivamente la richiedono — nella meningite
   come esclusione di massa prima della rachicentesi. Se siete d'accordo la portiamo a
   obbligatoria condizionale in entrambe.
5. **Una deroga alla vostra formulazione sulla FND, e la ragione.** Avete scritto «tutti i tool
   diagnostici opzionali». Abbiamo reso opzionale tutto lo strumentale tranne uno: la
   **video-EEG resta obbligatoria nei 22 casi su 30 con eventi paroxistici**. Non la
   consideriamo un esame di esclusione ma *l'atto diagnostico positivo* delle crisi non
   epilettiche psicogene: registrare un evento abituale senza correlato EEG è ciò che dà la
   certezza «documentata» secondo la Task Force ILAE 2013, e nessun segno clinico da letto lo
   sostituisce. Nei 30 casi si tratta di ricoveri fatti esattamente per quello. Negli altri 8
   casi, dove non ci sono eventi da registrare, la video-EEG non compare. Se preferite che sia
   opzionale anche lì, la declassiamo: è una riga di configurazione e 22 casi.
