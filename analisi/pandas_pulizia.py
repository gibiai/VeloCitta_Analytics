# Task 6.1 e 6.2 — Creazione DataFrame e pulizia dati
# Crea tre DataFrame e li pulisce

import pandas as pd
import numpy as np
from giorno_1.demo import classifica_corsa  # importa la funzione già scritta

np.random.seed(42)
pd.set_option("display.max_columns", None)  # mostra tutte le colonne nel print

# 6.1 — CREAZIONE DATAFRAME
print("TASK 6 — Pandas: Pulizia e Analisi")
print("-" * 40)

# dati di riferimento
citta         = ["Milano", "Roma", "Torino"]
fasce_orarie  = ["mattina", "pomeriggio", "sera", "notte"]
tipi_bici     = ["classica", "elettrica"]
abbonamenti   = ["Base", "Premium", "Family"]

# df_corse — almeno 80 righe
# costruisce le colonne una per una con liste e random
# poi passa tutto a pd.DataFrame come dizionario
n_corse = 85  # sopra il minimo richiesto

id_corse      = [f"C{i:04d}" for i in range(1, n_corse + 1)]  # C0001, C0002...
id_bici_corse = [f"B{np.random.randint(1, 21):03d}" for _ in range(n_corse)]
id_utenti_c   = [f"U{np.random.randint(1, 26):03d}" for _ in range(n_corse)]
citta_corse   = np.random.choice(citta, size=n_corse).tolist()
date_corse    = np.random.choice(
    ["2026-03-01", "2026-03-15", "2026-04-10"], size=n_corse
).tolist()
durate_corse  = np.random.randint(5, 90, size=n_corse).tolist()
km_corse      = [round(d * np.random.uniform(0.15, 0.25), 2) for d in durate_corse]
fasce_c       = np.random.choice(fasce_orarie, size=n_corse).tolist()

df_corse = pd.DataFrame({
    "id_corsa":      id_corse,
    "id_bici":       id_bici_corse,
    "id_utente":     id_utenti_c,
    "citta":         citta_corse,
    "data_corsa":    date_corse,
    "durata_minuti": durate_corse,
    "km_percorsi":   km_corse,
    "fascia_oraria": fasce_c,
})

# 5 duplicati — copie delle prime 5 righe
duplicati = df_corse.iloc[:5].copy()
df_corse  = pd.concat([df_corse, duplicati], ignore_index=True)

# 8 NaN sparsi tra durata_minuti e km_percorsi
indici_nan_durata = np.random.choice(df_corse.index, size=4, replace=False)
indici_nan_km     = np.random.choice(df_corse.index, size=4, replace=False)
df_corse.loc[indici_nan_durata, "durata_minuti"] = np.nan
df_corse.loc[indici_nan_km,     "km_percorsi"]   = np.nan

# df_bici — almeno 20 righe
n_bici = 20

df_bici = pd.DataFrame({
    "id_bici":        [f"B{i:03d}" for i in range(1, n_bici + 1)],
    "tipo":           np.random.choice(tipi_bici, size=n_bici).tolist(),
    "citta":          np.random.choice(citta, size=n_bici).tolist(),
    "anno_acquisto":  np.random.randint(2018, 2025, size=n_bici).tolist(),
    "costo_acquisto": np.random.choice([800, 1200, 1500, 2000], size=n_bici).tolist(),
})

# df_utenti — almeno 25 righe
nomi = ["Luca", "Sara", "Marco", "Giulia", "Anna", "Paolo", "Elena",
        "Matteo", "Chiara", "Roberto", "Alessia", "Davide", "Martina",
        "Simone", "Francesca", "Andrea", "Valentina", "Giovanni", "Laura",
        "Stefano", "Beatrice", "Lorenzo", "Sofia", "Michele", "Federica"]

df_utenti = pd.DataFrame({
    "id_utente":        [f"U{i:03d}" for i in range(1, 26)],
    "nome":             nomi,
    "citta":            np.random.choice(citta, size=25).tolist(),
    "tipo_abbonamento": np.random.choice(abbonamenti, size=25).tolist(),
    "data_iscrizione":  np.random.choice(
        ["2024-01-15", "2024-06-01", "2025-03-20"], size=25
    ).tolist(),
})

print("\n--- 6.1 DataFrame creati ---")
print(f"df_corse:  {df_corse.shape[0]} righe, {df_corse.shape[1]} colonne")
print(f"df_bici:   {df_bici.shape[0]} righe, {df_bici.shape[1]} colonne")
print(f"df_utenti: {df_utenti.shape[0]} righe, {df_utenti.shape[1]} colonne")

print("\nPrime 5 righe df_corse:")
print(df_corse.head())

# 6.2 — PULIZIA DATI
print("\n--- 6.2 Pulizia dati ---")

# info e describe PRIMA della pulizia
print("\n.info() PRIMA della pulizia:")
df_corse.info()
print("\n.describe() PRIMA della pulizia:")
print(df_corse.describe())

# rimozione duplicati
righe_prima = len(df_corse)
df_corse    = df_corse.drop_duplicates()
righe_dopo  = len(df_corse)
print(f"\nDuplicati rimossi: {righe_prima - righe_dopo} righe")
print(f"Righe rimaste: {righe_dopo}")

# valori mancanti
print("\nValori mancanti prima del fillna:")
print(df_corse.isnull().sum())

# durata_minuti NaN -> mediana per città
# raggruppa per città
# calcola la mediana per ogni gruppo ma
# RESTITUISCE UN VALORE PER OGNI RIGA ORIGINALE (non riduce il DataFrame)
df_corse["durata_minuti"] = df_corse["durata_minuti"].fillna(
    df_corse.groupby("citta")["durata_minuti"].transform("median")
)

# km_percorsi NaN -> durata_minuti * 0.18
# dove km è NaN, calcola una stima dal tempo della corsa
df_corse["km_percorsi"] = df_corse["km_percorsi"].fillna(
    df_corse["durata_minuti"] * 0.18
).round(2)
print("\nValori mancanti dopo il fillna:")
print(df_corse.isnull().sum())

# conversione date
# converte la stringa "2026-03-01" in un oggetto datetime
df_corse["data_corsa"] = pd.to_datetime(df_corse["data_corsa"])

# estrae mese e giorno della settimana dalla data
# .dt è "l'accessor" per le operazioni datetime sulle Series
df_corse["mese"]            = df_corse["data_corsa"].dt.month
df_corse["giorno_settimana"] = df_corse["data_corsa"].dt.strftime("%A")  # es. "Monday"

# info e describe DOPO la pulizia
print("\n.info() DOPO la pulizia:")
df_corse.info()
print("\n.describe() DOPO la pulizia:")
print(df_corse.describe())

# salvataggio intermedio
# salviamo i DataFrame puliti in CSV per usarli in pandas_analisi.py
df_corse.to_csv("output/df_corse_pulito.csv",   index=False, encoding="utf-8")
df_bici.to_csv("output/df_bici.csv",            index=False, encoding="utf-8")
df_utenti.to_csv("output/df_utenti.csv",        index=False, encoding="utf-8")
print("\nDataFrame salvati in output/")