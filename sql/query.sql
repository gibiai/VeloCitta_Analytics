-- ─── D1 ───────────────────────────────────────────────────────────────────────
-- Tutte le corse a Milano ordinate per data decrescente.
-- Mostra: id_corsa, id_bici, data_corsa, durata_minuti.
--
-- Spiegazione:
-- SELECT sceglie le colonne da mostrare.
-- FROM corse indica la tabella sorgente.
-- WHERE filtra solo le corse dove la bici appartiene a Milano 
-- per sapere la città della bici serve un JOIN con la tabella biciclette.
-- ORDER BY data_corsa DESC ordina dal più recente al più vecchio
-- (DESC = decrescente, ASC = crescente).

SELECT
    c.id_corsa,
    c.id_bici,
    c.data_corsa,
    c.durata_minuti
FROM corse c
JOIN biciclette b ON c.id_bici = b.id_bici   -- colleghiamo corse e biciclette sull'id
WHERE b.citta = 'Milano'                       -- filtriamo solo le bici di Milano
ORDER BY c.data_corsa DESC;                    -- dalla corsa più recente alla più vecchia


-- ─── D2 ───────────────────────────────────────────────────────────────────────
-- Quante bici elettriche per ogni città?
-- Ordina dalla città con più bici a quella con meno.
--
-- Spiegazione:
-- WHERE tipo = 'elettrica' filtra solo le bici elettriche.
-- GROUP BY citta raggruppa le righe per città.
-- COUNT(*) conta quante righe ci sono in ogni gruppo.
-- ORDER BY COUNT(*) DESC ordina dal numero più alto al più basso.

SELECT
    citta,
    COUNT(*) AS n_bici_elettriche   -- conta le bici per ogni città
FROM biciclette
WHERE tipo = 'elettrica'            -- solo bici elettriche
GROUP BY citta                      -- una riga per ogni città
ORDER BY n_bici_elettriche DESC;    -- dalla città con più bici a quella con meno


-- ─── D3 ───────────────────────────────────────────────────────────────────────
-- Durata media, massima e minima per tipo di bicicletta. (JOIN richiesto)
--
-- Spiegazione:
-- La tabella corse non ha il tipo di bici, lo ha la tabella biciclette.
-- Il JOIN unisce le due tabelle sull'id_bici comune.
-- GROUP BY b.tipo raggruppa per tipo (classica / elettrica / cargo).
-- AVG, MAX, MIN calcolano le statistiche su durata_minuti per ogni gruppo.

SELECT
    b.tipo,                                    -- tipo di bicicletta
    ROUND(AVG(c.durata_minuti), 2) AS durata_media,   -- media arrotondata a 2 decimali
    MAX(c.durata_minuti)           AS durata_max,
    MIN(c.durata_minuti)           AS durata_min
FROM corse c
JOIN biciclette b ON c.id_bici = b.id_bici    -- JOIN per ottenere il tipo dalla tabella bici
GROUP BY b.tipo;                               -- una riga per ogni tipo di bici


-- ─── D4 ───────────────────────────────────────────────────────────────────────
-- Stazioni di Milano con più di 50 arrivi in aprile 2026.
-- Ordina per conteggio decrescente.
--
-- Spiegazione:
-- Conta gli arrivi raggruppando per stazione_arrivo.
-- HAVING filtra i gruppi DOPO il GROUP BY, equivale a WHERE ma sui risultati aggregati.
-- Non possiamo usare WHERE COUNT(*) > 50 perché WHERE viene applicato prima
-- del GROUP BY, prima ancora che i conteggi esistano.
-- BETWEEN filtra le date in un intervallo inclusi gli estremi.

SELECT
    c.stazione_arrivo,
    COUNT(*) AS n_arrivi
FROM corse c
JOIN stazioni s ON c.stazione_arrivo = s.nome  -- JOIN per filtrare per città stazione
WHERE s.citta = 'Milano'                        -- solo stazioni di Milano
  AND c.data_corsa BETWEEN '2026-04-01' AND '2026-04-30'  -- solo aprile 2026
GROUP BY c.stazione_arrivo                      -- una riga per stazione
HAVING COUNT(*) > 50                            -- solo stazioni con più di 50 arrivi
ORDER BY n_arrivi DESC;                         -- dalla stazione con più arrivi


-- ─── D5 ───────────────────────────────────────────────────────────────────────
-- Utenti "Premium" con almeno 10 corse.
-- Mostra numero corse totali e km totali. (JOIN richiesto)
--
-- Spiegazione:
-- JOIN tra corse e utenti per ottenere il tipo_abbonamento.
-- WHERE filtra solo gli utenti Premium.
-- GROUP BY u.id_utente raggruppa le corse per utente.
-- HAVING COUNT(*) >= 10 tiene solo gli utenti con almeno 10 corse.
-- SUM(c.km_percorsi) somma i km di tutte le corse di ogni utente.

SELECT
    u.id_utente,
    u.nome,
    COUNT(c.id_corsa)      AS n_corse,       -- numero corse totali
    ROUND(SUM(c.km_percorsi), 2) AS km_totali  -- km percorsi in totale
FROM corse c
JOIN utenti u ON c.id_utente = u.id_utente   -- JOIN per ottenere dati utente
WHERE u.tipo_abbonamento = 'Premium'          -- solo utenti Premium
GROUP BY u.id_utente, u.nome                 -- una riga per utente
HAVING COUNT(c.id_corsa) >= 10               -- solo utenti con almeno 10 corse
ORDER BY km_totali DESC;                     -- dal più attivo al meno attivo


-- ─── D6 ───────────────────────────────────────────────────────────────────────
-- COSA FA:
-- Questa query calcola per ogni stazione il numero di arrivi, il numero di
-- partenze e il "bilancio" (arrivi - partenze).
--
-- COME FUNZIONA:
-- Usa due LEFT JOIN sulla stessa tabella corse con due alias diversi:
--   c_in  -> rappresenta le corse in ARRIVO (stazione_arrivo = nome stazione)
--   c_out -> rappresenta le corse in PARTENZA (stazione_partenza = nome stazione)
-- LEFT JOIN garantisce che ogni stazione appaia nel risultato anche se
-- non ha arrivi o partenze, in quel caso COUNT restituisce 0.
-- GROUP BY raggruppa per stazione e città.
-- ORDER BY bilancio DESC mette in cima le stazioni con più arrivi che partenze.
--
-- INFORMAZIONE DI BUSINESS:
-- Il bilancio positivo indica stazioni dove le bici si accumulano
-- (più persone che arrivano piuttost che partono), sono stazioni che rischiano di
-- saturarsi e richiedono redistribuzione delle bici verso altre stazioni.
-- Il bilancio negativo indica stazioni che si svuotano, rischiano di
-- rimanere senza bici disponibili.
-- Analisi fondamentale per ottimizzare la distribuzione della flotta
-- in un sistema di bike sharing.

SELECT
    s.nome    AS stazione,
    s.citta,
    COUNT(c_in.id_corsa)                                AS arrivi,
    COUNT(c_out.id_corsa)                               AS partenze,
    COUNT(c_in.id_corsa) - COUNT(c_out.id_corsa)        AS bilancio
FROM stazioni s
LEFT JOIN corse c_in  ON s.nome = c_in.stazione_arrivo    -- conta le corse arrivate
LEFT JOIN corse c_out ON s.nome = c_out.stazione_partenza -- conta le corse partite
GROUP BY s.nome, s.citta
ORDER BY bilancio DESC;                                    -- stazioni più sature in cima
