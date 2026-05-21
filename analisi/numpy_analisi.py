# Task 5 - Analisi numerica con NumPy
# simula 500 corse di bike sharing e produce:
# 5.1 - Generazione Dati (durate, km, velocità)
# 5.2 - Slicing, fancy indexing e maschere bool
# 5.3 - Statistiche e normalizzazione min-max
# 5.4 - Serie temporale simulata con media mobile a 7 giorni

import numpy as np

np.random.seed(42) # garantisce numeri casuali sempre gli stessi

# 5.1 Generazione Dati

# durate
# genera valori distribuzione normale
# simulazione corse con durata media di 28 min
# clip gestisce min max insieme
durate_raw = np.random.normal(28, 12, size=500)   # 500 valori decimali
durate = durate_raw.astype(int)                     # converti in interi
durate = np.clip(durate, 1, None)                   # nessuna durata < 1 minuto

# km percorsi
# genera valori decimali casuali uniformi
# moltiplichiamo durate per fattore casuale tra 0.15 e 0.25
fattore_km = np.random.uniform(0.15, 0.25, size=500)
km = durate * fattore_km
km = np.around(km, 2) # arrotonda ogni elemento a 2 decimali

# velocità
# velocità = km / ore = km / (minuti / 60)
# converte durate da minuti in ore con broadcasting su tutti elementi
velocità = km / (durate / 60) # risultato km/h per ogni corsa

# riepologo shape, dtype e statistiche
print("\n--- 5.1 Generazione Dati ---")
for nome, arr in [("durate", durate), ("km", km), ("velocità", velocità)]:
    print(f"\n{nome}:")
    print(f"  shape: {arr.shape} | dtype: {arr.dtype}")
    print(f"  min: {arr.min():.2f} | max: {arr.max():.2f} | "
          f"media: {arr.mean():.2f} | std: {arr.std():.2f}")

# 5.2 Slicing e selezione
print("\n--- Slicing e selezione ---")
# prime e ultime 10 ore
prime_10 = durate[:10] # prime 10 corse (da 0 a 9)
ultime_10 = durate[-10:] # ultime 10 corse
print(f"\nPrime 10 durate:  {prime_10}")
print(f"Ultime 10 durate: {ultime_10}")

# Fancy Indexing 
indici_specifici = [0, 42, 99, 150, 200, 350, 499]
selezione = durate[indici_specifici]   # fancy indexing
print(f"\nFancy indexing (indici {indici_specifici}):")
print(f"  {selezione}")

# Maschera Booleana
# crea un array T/F per ogni elemento
maschera_lunghe = durate > 45                    # array di True/False
corse_lunghe    = durate[maschera_lunghe]         # solo le corse > 45 min
km_corse_lunghe = km[maschera_lunghe]             # km delle corse lunghe
print(f"\nCorse con durata > 45 min: {len(corse_lunghe)} su {len(durate)}")
print(f"Distanza media corse lunghe: {km_corse_lunghe.mean():.2f} km")

# Indice velocità minima e massima
# argmax - argmin restituiscono posizione valore, non valore stesso
idx_max_vel = np.argmax(velocità)   # indice velocità massima
idx_min_vel = np.argmin(velocità)   # indice velocità minima
print(f"\nVelocità massima: {velocità[idx_max_vel]:.2f} km/h (corsa #{idx_max_vel})")
print(f"Velocità minima:  {velocità[idx_min_vel]:.2f} km/h (corsa #{idx_min_vel})")

# 5.3 Statistiche e Normalizzazione
print("\n--- 5.3 Statistiche e Normalizzazione")

# percentili
# np.percentile(array, q) calcola il percentile q
# il 25° percentile è il valore sotto cui cade il 25% dei dati
# il 50° è la mediana, il 75° e 90° indicano la coda della distribuzione
p25, p50, p75, p90 = np.percentile(durate, [25, 50, 75, 90])
print(f"\nPercentili durate:")
print(f" 25°: {p25:.1f} min | 50°: {p50:.1f} min | "
      f"75°: {p75:.1f} min | 90°: {p90:.1f} min")

# normalizzazione min - max
# formula: (x - min) / (max - min)
# porta tutti i valori nell'intervallo [0, 1]
# il valore minimo diventa 0, il massimo diventa 1
# operazione vettoriale — applicata a tutti i 500 elementi in una riga
durate_norm = (durate - durate.min()) / (durate.max() - durate.min())

# verifica che tutti i valori siano effettivamente tra 0 e 1
min_norm = durate_norm.min()
max_norm = durate_norm.max()

print(f"\nNormalizzazione min-max durate:")
print(f"  min normalizzato: {min_norm:.4f} (atteso: 0.0)")
print(f"  max normalizzato: {max_norm:.4f} (atteso: 1.0)")
print(f"  media normalizzata: {durate_norm.mean():.4f}")

if min_norm < 0 or max_norm > 1:
    print("ATTENZIONE: valori fuori range [0, 1]!")
else:
    print("Tutti i valori sono in [0, 1]")
    
# ── correlazione di Pearson ───────────────────────────────────────────────────
# misura quanto due variabili si muovono insieme — da -1 a +1
# +1 = correlazione perfetta positiva (una sale, l'altra sale sempre)
# 0 = nessuna relazione
# -1 = correlazione perfetta negativa (una sale, l'altra scende sempre)
# ci aspettiamo un valore alto: corse più lunghe → più km percorsi
matrice_corr = np.corrcoef(durate, km) # matrice 2x2 di correlazioni
corr_durate_km = matrice_corr[0, 1]   # elemento riga 0, colonna 1 correlazione tra durate e km
print(f"\nCorrelazione di Pearson durate ↔ km: {corr_durate_km:.4f}")
print(f"  → {'Correlazione alta' if corr_durate_km > 0.7 else 'Correlazione moderata'}: "
      f"corse più lunghe percorrono più km, come atteso.")

# 5.4 Serie Temporale Simulata
print("\n--- 5.4 Serie temporale (30 giorni) ---")

# generazione corse giornaliere
# simula numero di corse per ognuno dei 30 giorni
corse_giornaliere = np.random.randint(80, 200, size=30) # # min=80, max=200: tra 80 e 199 corse al giorno

# media mobile a 7 giorni
# calcoliamoi media per ogni giorni degli ultimi 7 giorni incluso oggi
# attenua oscillazioni e mostra trend generale
# primi 6 giorni -> None
media_mobile = []
for giorno in range(30):
    if giorno < 6:
        # giorni 0-5: meno di 7 giorni disponibili, dato mancante
        media_mobile.append(None)
    else:
        # slicing: prendi i 7 giorni da (giorno-6) fino a (giorno) incluso
        # ricorda: stop è ESCLUSO nello slicing (giorno+1)
        ultimi_7 = corse_giornaliere[giorno - 6 : giorno + 1]
        media_7  = ultimi_7.mean()             # .mean() su un array NumPy
        media_mobile.append(round(media_7, 1)) # arrotonda a 1 decimale

# picco massimo e minimo
giorno_max = np.argmax(corse_giornaliere) + 1
giorno_min = np.argmin(corse_giornaliere) + 1
 
print(f"\nPicco massimo: giorno {giorno_max} "
      f"con {corse_giornaliere[giorno_max - 1]} corse")
print(f"Picco minimo:  giorno {giorno_min} "
      f"con {corse_giornaliere[giorno_min - 1]} corse")

# tabella riepilogativa
# stampiamo tabella con giorno, corse e media mobile
# :>N allinea il testo a destra in N spazi, per colonne ordinate
# per i primi 6 giorni "  —  "
print(f"\n{'Giorno':>7} | {'Corse':>6} | {'Media 7gg':>9}")
print("-" * 30)
for giorno in range(30):
    corse = corse_giornaliere[giorno]
    media = media_mobile[giorno]
    media_str = f"{media:>9.1f}" if media is not None else "      —  "
    print(f"{giorno + 1:>7} | {corse:>6} | {media_str}")