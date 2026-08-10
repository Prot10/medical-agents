# Reply to Flavia and Antonio — tool review round 1

Ready to send. Italian, matching the thread. Delete this file once sent.

Before sending, three things only Andrea can settle:

1. **Section 8 is an ask, not a report.** It lists clinical text we composed and asks them to check
   it. If you would rather not surface that in this letter, it has to move somewhere they will
   actually read it — it must not simply disappear.
2. **The timeline in section 9.** It says the three new conditions are not built yet. Put a real date
   on it or remove the sentence; do not promise a week we have not planned.
3. Whether to send now or wait for the deploy. The letter says the platform is up to date; that is
   only true after `deployment/hostinger/deploy.sh` runs. **Sending before the deploy makes the
   letter wrong** — they would log in and see the 10 July snapshot.

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
  ciascun caso già documentava: Hoover in 21 casi più 2 equivoci, miglioramento con distrazione in 20, cedimento
  (give-way) in 17, andatura trascinata in 16, incoerenza al riesame in 15, dissociazione
  sensitiva non anatomica in 14, sulla linea mediana in 10, entrainment del tremore in 9. Nei 3
  casi puramente parossistici, dove i segni sugli arti non si applicano, il referto porta la
  semeiologia dell'evento e dice esplicitamente che l'atto diagnostico positivo è la
  registrazione video-EEG;
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
- risultato: negli 8 casi senza eventi parossistici il percorso obbligatorio costa **138 EUR** e
  nei 22 con eventi 1 242 EUR, contro **2 426 EUR** del percorso difendibile completo: è quel
  divario che rende misurabile l'*overuse*, non il costo assoluto.

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

- **I 18 cambi di tier e le 6 rimozioni: applicati, e vi raccontiamo un errore nostro.** Li
  avevamo applicati al pannello di generazione, che è anche quello che alimenta il catalogo che
  avete letto — ma il tier che il benchmark *misura* sta nel singolo caso. Verificando, abbiamo
  trovato che 13 dei 18 esistevano solo nel pannello: cambiati dove si legge, non dove si misura.
  È la stessa forma dell'errore del punto 3, e ora sono nei casi tutti tranne due, che vi chiediamo
  di confermare (la TC cranio nell'encefalopatia epatica e nella meningite: 30 e 27 casi la
  richiedono, nella meningite come esclusione di massa prima della rachicentesi, e togliere un passo
  di esclusione prima di una procedura invasiva sulla nostra sola lettura non ci pareva corretto).
- **Gli atti clinici che ci avevate indicato come obbligatori sono ora nei casi**, non solo nel
  pannello: valutazione cognitiva strutturata in Alzheimer e FTD (60 casi), anamnesi ICHD-3
  nell'emicrania (30), marcia e cognizione cronometrate prima e dopo il tap test nella NPH (30),
  acquisizione tissutale con diagnosi istomolecolare integrata nel glioma (30), telemetria continua
  nella GBS (30). I passi obbligatori da pannello assenti dai casi erano 211: ora sono 28, e tutti
  e 28 sono esenzioni dichiarate con la motivazione clinica: 27 sono casi di ESA in cui la TC è
  diagnostica — la rachicentesi resta obbligatoria nei 3 con TC negativa — e il ventottesimo è il
  caso di demenza vascolare con pacemaker non compatibile, in cui la RM è controindicata.
- **Due cose che questo lavoro ha fatto emergere e che vale la pena dirvi.** Nell'emicrania il
  declassamento della RM era stato applicato a metà dei casi e l'anamnesi ICHD-3 a nessuno: in 15
  casi l'insieme obbligatorio conteneva soltanto i due strumenti a costo zero, e un agente prendeva
  copertura piena **senza compiere un solo atto diagnostico**. E nel glioma la neuropatologia con il
  pannello molecolare c'era in tutti e 30 i casi, ma archiviata come esito del tool di laboratorio:
  la diagnosi integrata era ottenibile ordinando gli esami del sangue, e nessuna azione richiedeva
  il prelievo di tessuto. Il vostro rilievo era esatto e la ragione per cui non si vedeva è che il
  risultato stava sotto il tool sbagliato. Entrambi corretti, e ora c'è un controllo automatico che
  blocca il ripetersi di entrambi.
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
- **La vostra obiezione sui "secchielli generici" era anche un buco nel punteggio, e l'abbiamo
  chiuso.** Il ground truth conteneva già il dettaglio per singolo analita, ma il punteggio
  riconosceva solo il nome del tool: chi ordinava «dosaggio del valproato» — l'ordine
  clinicamente corretto — non prendeva credito per una richiesta di «livelli di antiepilettici»,
  mentre chi ordinava il termine vago sì. Ora l'ordine specifico soddisfa la richiesta di classe,
  **ma non il contrario**: una richiesta di esame specifico non è mai coperta dal nome generico.
  La vaghezza non deve diventare il modo più economico di segnare punti.
- **Le vostre descrizioni condizione-specifiche ora sono in piattaforma, sotto la riga a cui le
  avete scritte, con accanto la nostra risposta.** Questo era il punto in cui vi stavamo per dire
  una cosa vaga, e ve lo raccontiamo perché il difetto era strutturale. Il testo che avete scritto
  è *per patologia* («per la SM, RM encefalo **e midollo** con protocollo SM»), mentre il catalogo
  aveva una sola descrizione per tool, mostrata identica in tutte e 20 le patologie: quel testo non
  aveva letteralmente un posto dove stare. Non poteva nemmeno andare nella descrizione che legge
  l'agente, perché un'indicazione condizione-specifica gli regala la diagnosi che deve inferire.
  Risultato: la sostanza delle vostre riscritture era arrivata dove viene *misurata* (vocabolario e
  ground truth), ma il testo che avreste riletto era ancora quello vecchio su tre tool — RM
  encefalo, EEG e test specialistici — che da soli raccolgono **35 delle vostre 91 annotazioni**.
  Avreste ritrovato parola per parola la stringa che avevate chiesto di cancellare.

  Adesso esiste un livello dedicato: **110 voci** (le 91 annotazioni, più 19 perché alcune
  contengono due item distinti), ognuna con il vostro testo, la vostra motivazione, la vostra
  fonte, **e cosa abbiamo fatto**, con un'etichetta di stato che vi dice dove guardare:

  | Stato | Voci | Cosa significa |
  |---|---:|---|
  | applicato | 89 | i casi e il vocabolario si comportano come chiedete |
  | serve la vostra decisione | 9 | abbiamo fatto qualcosa di diverso da quanto chiesto, e lo dichiariamo |
  | applicato in parte | 6 | il tool esiste, i casi che dovrebbero usarlo non sono ancora scritti |
  | nessuna modifica richiesta | 4 | — |
  | domanda aperta | 1 | la FND (punto 2) |
  | patologia ritirata | 1 | la neuropatia periferica |

  Undici delle vostre annotazioni descrivono esami che nello spazio d'azione a 12 tool non
  esistevano, e le avevate quindi appoggiate alla riga più vicina: lo screening del teratoma sotto
  la RM encefalo, le emocolture sotto il laboratorio, la biopsia del glioma sotto la RM. Ora il
  vostro testo compare sul tool che esegue davvero l'esame, con l'indicazione di dove l'avevate
  scritto — così vedete che non è stato perso.

  Abbiamo anche riscritto le tre descrizioni condivise rimaste intatte. Quella dei test
  specialistici era il vostro «too broad» in cinque patologie: ora elenca i 19 esami reali
  raggruppati, con la regola che **il valore scelto è ciò che viene fatturato e valutato**, non la
  categoria. E il vostro EEG deprivato di sonno nell'epilessia temporale **non esisteva come esame
  ordinabile**: ora è tariffato (276 EUR, CPT 95819) e deriva automaticamente nel vocabolario, nel
  catalogo e nel tracciamento costi.

  Un ultimo effetto collaterale, che vale come prova che il metodo serve: rispondere a una
  annotazione per volta ci ha costretti a scoprire **quattro casi in cui la risposta che stavamo per
  darvi era falsa** — l'eco e il monitoraggio cardiaco nell'epilessia temporale erano rimasti a
  *recommended* e non opzionali come vi stavamo scrivendo, e nella NPH la batteria
  neuropsicologica era ancora obbligatoria in tutti e 30 i casi accanto alla nuova valutazione
  pre/post, che è esattamente la duplicazione che avevate chiesto di togliere. Corretti.

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

Un punto separato, e qui abbiamo cambiato idea due volte prima di darvi una risposta. Nei tre
casi di emicrania in cui l'ecocardiogramma è **required** siamo andati a leggere la diagnosi, e
nessuno dei tre è un'emicrania di routine: **MIG-AURA-P03** è un infarto migrainoso la cui
diagnosi si regge sull'aver escluso le cause secondarie, **MIG-AURA-P07** è un ictus
cardioembolico che il caso dichiara *non* essere un infarto migrainoso, e **MIG-AURA-P08** è una
MELAS con mutazione confermata, dove lo screening della cardiomiopatia è standard. In tutti e tre
l'eco è ricerca della fonte embolica o screening cardiologico, non un test per l'emicrania.
Quindi resta, e la domanda che vi giriamo è un'altra: se quei casi possano stare sotto
l'etichetta «emicrania con aura» o se vadano spostati. Stessa logica per la video-EEG in
**MIG-AURA-RM11**, la cui diagnosi comprende una *migralepsia* — una crisi durante l'aura, ICHD-3
1.4.4 — quindi l'EEG stabilisce metà della diagnosi e non è valutazione di routine della cefalea.

## 6. Miastenia gravis

Le cinque annotazioni che avete inserito sotto "Peripheral neuropathy" riguardano in realtà
la miastenia gravis (anti-AChR/anti-MuSK, SFEMG, imaging del mediastino, Evoli 2019 e
Jacob 2025). Le abbiamo spostate sotto **Myasthenia gravis**, che altrimenti sarebbe rimasta
l'unica condizione senza review. Se non era intenzionale, fatecelo sapere e le rimettiamo
dove erano.

Vale la pena dirvi cosa ha prodotto quello spostamento, perché è la dimostrazione più netta del
valore della vostra review. Andando a verificare la MG proprio grazie alle vostre cinque
annotazioni, abbiamo trovato che in **tutti e 9** i casi che archiviano un pannello
anti-recettore dell'acetilcolina il referto era **irraggiungibile**: l'azione obbligatoria ordina
`anti-AChR`, `anti-MuSK`, `anti-LRP4`, TSH — i nomi degli analiti — mentre il risultato era
archiviato sotto un'etichetta che nominava la malattia. Nessun termine in comune, quindi nessuna
chiamata lo raggiungeva. Otto casi rispondevano con un pannello di esclusione; uno rispondeva con
il **pannello anti-gangliosidi di Miller-Fisher**, cioè l'anticorpo di un'altra malattia. In
pratica il benchmark chiedeva di confermare sierologicamente la miastenia e non consegnava la
sierologia. Corretto in tutti e nove, senza toccare una virgola dei referti.

## 7. Abbiamo riletto i 600 casi uno per uno, e dobbiamo dirvi cosa abbiamo trovato

Applicando le vostre correzioni ci siamo accorti che alcune non si vedevano nei casi perché il
*risultato* stava sotto il tool sbagliato (il glioma del punto 4 è l'esempio). Ci è sembrato che
quel difetto non potesse essere isolato, quindi abbiamo fatto una cosa che avremmo dovuto fare
prima di consegnarvi il dataset: abbiamo riprodotto **ogni singola azione del percorso ideale**
contro il simulatore e controllato che il referto restituito contenesse davvero il risultato che
l'azione chiede.

Il punto che vi interessa più di tutti: **i controlli automatici erano verdi tutto il tempo.**
Erano verdi anche quando la miastenia non consegnava la sua sierologia. Verificano che ogni caso
sia coerente con se stesso, non che il simulatore risponda alla domanda posta. Nessuno dei difetti
sotto sarebbe stato intercettato.

Quelli che pesano clinicamente:

- **In 21 casi di ictus ischemico su 30 non esisteva alcuna TC senza contrasto.** È l'esame che
  esclude l'emorragia prima della trombolisi, cioè la decisione per cui quella condizione esiste
  nel benchmark.
- **Nell'ESA angio-TC e angiografia digitale erano incrociate**: 30 angio-TC archiviate sotto
  un'etichetta che nominava la DSA e 3 referti DSA sotto etichette che nominavano l'angio-TC. In più
  54 angiografie obbligatorie non erano raggiungibili dalla chiamata che le nomina, perché
  l'angiografia si ordina con un flag e il simulatore leggeva solo i valori. E l'**angiografia
  cerebrale non esisteva nemmeno nel listino**: c'era quella coronarica, non quella cerebrale. Ora
  c'è, tariffata.
- **In 28 casi il patogeno era ottenibile da un esame del sangue**: le emocolture erano archiviate
  dentro l'esito del laboratorio, quindi l'organismo — il dato che nomina il patogeno e seleziona
  l'antibiotico — arrivava senza fare microbiologia.
- **21 referti microbiologici nominavano l'isolato e poi lo negavano** («nessuna crescita» con
  l'organismo indicato nel campo accanto).
- **In 31 casi lo stesso paziente aveva due o tre punteggi diversi sullo stesso strumento** — tutti
  e 30 i FND più un FTD: PHQ-9 6 contro 14 contro 17, GAD-7 5 contro 14 contro 16, su fasce di
  gravità differenti e senza alcuna nota di somministrazione ripetuta. Quale valore vedesse
  l'agente dipendeva dall'ordine in cui chiamava gli strumenti. In più, 34 output archiviavano una
  valutazione psichiatrica dentro il tool di laboratorio — PHQ-9, GAD-7, DES-II, PCL-5, diagnosi
  DSM-5 e narrativa d'intervista impacchettati come «pannello» di esami, uno con unità di misura
  «diagnosi» e un «test» chiamato *Trauma history* il cui valore è un paragrafo. In FND-M09
  l'unico esame di laboratorio previsto è uno screening opzionale delle cause reversibili, quindi
  un agente che chiedeva gli esami del sangue si vedeva restituire una valutazione psichiatrica.
  Il ground truth non fissa nessun punteggio, quindi scegliere uno dei due avrebbe significato
  inventare una misura: il difetto sta a monte del numero, e la correzione è una sola
  somministrazione, nel tool che la esegue.
- **Un test legato al cromosoma X era ordinato in 11 pazienti di sesso femminile.**
- **41 "distrattori" dichiarati puntavano a campi inesistenti**, quindi non distraevano nessuno.
- **13 casi di meningite fatturavano un pannello PCR multiplex (322 EUR) che nessun caso
  restituiva** — e in 9 di quei 13 il Gram è negativo e la coltura ancora in corso, cioè
  esattamente la situazione in cui quel pannello è l'unica identificazione disponibile.

Non lo scriviamo per farci perdonare: lo scriviamo perché cambia cosa vi stiamo chiedendo. La
frase che avevamo pronta per voi — «i casi passano i controlli automatici, quindi quello che
segnalerete sarà sostanza clinica» — **era sbagliata**, e adesso lo sappiamo con precisione.
Passare i controlli non significava essere clinicamente solidi.

## 8. Testo clinico che abbiamo scritto noi, e che vi chiediamo di controllare

Riparando i difetti del punto 7 in alcuni casi non bastava spostare un referto: bisognava
**scrivere un risultato che non c'era**. Abbiamo seguito una regola sola — un caso che afferma una
diagnosi afferma con essa che gli esami ordinati per escludere le alternative non ne hanno mostrata
una, quindi riportarlo è riportare la posizione del caso; un numero, invece, sarebbe inventarlo.
Non abbiamo mai scritto un valore numerico che il caso non contenesse già.

Questa è la parte del dataset che più ha bisogno del vostro occhio, perché è l'unica in cui il
contenuto clinico l'abbiamo prodotto noi:

| Cosa | Dove | Cosa vi chiediamo |
|---|---|---|
| **Pannello PCR della meningite**, 13 casi | referto liquorale | L'organismo lo stabilisce il caso stesso (antigene latex, Gram, o identificazione colturale preliminare). Per *S. suis*, *Proteus mirabilis* e *Klebsiella* abbiamo scritto «nessun target rilevato» perché non sono target del pannello, aggiungendo che un pannello negativo non esclude una meningite batterica. **I target del pannello sono elencati nel referto** proprio perché possiate verificarli invece di fidarvi. |
| **421 righe di esclusione** in 190 casi | pannelli di laboratorio e liquor | Dicono «ordinato per escludere una causa alternativa; il risultato non ne indica una». Abbiamo lasciato fuori di proposito 128 esami che *confermano* la diagnosi (NfH nella SLA, Abeta42 nell'Alzheimer, bande oligoclonali nella SM, citologia nel glioma) e 8 dosaggi di antiepilettico, perché terapeutico contro subterapeutico è un numero con conseguenze. |
| **188 pannelli di base** in 135 casi | emocromo, metabolico, epatico, coagulazione, TSH, B12, HIV, gruppo e ricerca anticorpi irregolari | Refertati come non alterati **solo dove nulla nel caso dice il contrario** — nessun valore segnalato alterato in alcun output, niente nell'interpretazione, niente in ciò che il percorso ideale si aspetta, niente nell'anamnesi. Il gruppo sanguigno non è nominato: sarebbe stato inventare un dato del paziente, quindi riportiamo solo che la ricerca di anticorpi irregolari è negativa. Gli esami qualitativi mantengono una formulazione qualitativa (HIV «non reattivo», non «nei limiti»). |
| **Angiografia cerebrale** in 3 casi di ESA | azione + referto | Abbiamo dichiarato il termine e aggiunto l'azione solo nei 3 casi che hanno un referto DSA. Se secondo voi la DSA va richiesta in tutti i casi con angio-TC negativa e pattern emorragico diffuso (AHA/ASA 2023), ditecelo: è un giudizio sul singolo risultato angiografico e non ce lo siamo voluto arrogare. |

Due controlli automatici sorvegliano adesso questa parte, e vale la pena dire da dove vengono. Il
primo nasce dai 21 referti colturali del punto 7: un test blocca qualunque referto che neghi
l'isolato che il suo stesso campo nomina. È servito subito, perché la prima stesura del pannello
PCR della meningite elencava *Haemophilus influenzae* **sia** fra i rilevati **sia** fra i non
rilevati in un caso — intercettato prima di scrivere nulla sul dataset, ma è il tipo di errore che
un occhio clinico coglie e un controllo di contratto no. Il secondo ha rifiutato di scrivere
«emocromo nella norma» in undici casi in cui il caso descrive un'alterazione: otto Guillain-Barré
con pannello metabolico alterato, un'encefalite anti-NMDA e due stati epilettici. Senza quel
secondo controllo avremmo introdotto undici referti che contraddicono il proprio caso — cioè
esattamente il difetto che stavamo rimuovendo.

Su 600 casi restano **205 richieste di analiti senza risultato** (erano 742). Sono tutte
classificate: 93 sono gli esami confermativi e i dosaggi terapeutici lasciati fuori di proposito,
72 sono un nome di classe a cui il referto risponde con un suo membro (`autoimmune_panel` servito
con LGI1 e NMDAR), 32 richiedono un giudizio clinico caso per caso — 21 di queste sono
l'`anti-LRP4` nei casi di miastenia, dove il pannello referta AChR e MuSK — e 8 sono casi in cui il
caso afferma un'alterazione senza darne il valore. **Se su qualcuna di queste quattro categorie
avete un'opinione diversa, è il momento di dirlo**: sono decisioni nostre, non vincoli tecnici.

## 9. Prossimi passi

**Cosa è pronto adesso.** Le 20 patologie in piattaforma (600 casi, demenza vascolare compresa)
sono revisionabili da subito, con il catalogo dei tool corretto e le riparazioni dei punti 4, 7 e 8
applicate. Nella scheda **Tool** ogni riga patologia-esame ora porta un'etichetta «review»: aprendola
trovate il vostro commento, la vostra fonte e la nostra risposta. Le nove marcate **«serve la vostra
decisione»** sono i punti in cui abbiamo fatto qualcosa di diverso da quello che avevate chiesto:
sono la prima cosa da guardare, e bastano cinque minuti a testa. Il posto dove il vostro tempo rende
di più resta la sezione 8: è contenuto clinico che abbiamo scritto noi e su cui non esiste nessun
controllo automatico possibile.

**Cosa non è pronto.** Demenza a corpi di Lewy, emorragia intracerebrale spontanea ed encefalite
erpetica **non sono ancora in piattaforma**: mancano i pannelli e i 30 casi ciascuna. Preferiamo
dirvelo così invece di farvele trovare vuote. Prepariamo noi una prima versione dei pannelli (tier
e descrizioni) dalle linee guida che avete citato, e la troverete insieme ai casi, così la conferma
è parte della review e non un compito in più.

Una cosa che vi chiediamo di tenere presente mentre leggete: i controlli automatici passano su
600/600 casi, ma il punto 7 dice esattamente quanto poco questo garantisca. Trattate il verde come
l'assenza di difetti *di contratto*, non come una promessa di solidità clinica. Se qualcosa vi
sembra sbagliato, è più probabile che abbiate ragione voi.

Scusateci per l'attesa: siete rimasti fermi più di quanto fosse giusto, e la ragione è che abbiamo
preferito consegnarvi un dataset riparato piuttosto che farvi rifare la review su difetti nostri.

Grazie ancora — il livello di dettaglio dei vostri commenti sta cambiando il progetto in meglio, e
il punto 6 è la prova che anche un'annotazione finita nel posto sbagliato ha fatto emergere un
difetto che da soli non avremmo visto.

A presto,
Andrea
