# Task 6.3 & 6.4 - Apply, colonne derivate, aggregazioni e merge

import pandas as pd
import numpy as np
import sys
import os

# root del progetto per imporatare da giorno_1
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from giorno_1.demo import classifica_corsa

# caricamento DataFrame puliti da pandas_pulizia.py
df_corse = pd.read_csv("output/df_corse_pulito.csv", parse_dates=["data_corsa"])
df_bici = pd.read_csv("output/df_bici.csv")
df_utenti = pd.read_csv("output/df_utenti.csv")

print(f"\nDataFrame caricati: {len(df_corse)} corse, {len(df_bici)} bici, {len(df_utenti)} utenti")

# 6.3 Apply e Colonne Derivate
print("\n--- 6.3 Apply e colonne derivate ---")

# tipo corsa con apply
df_corse["tipo_corsa"] = df_corse["durata_minuti"].apply(classifica_corsa)
print("\nDistribuzione tipo corsa:")
print(df_corse["tipo_corsa"].value_counts())

# velocità media
df_corse["velocita_media"] = (df_corse["km_percorsi"] / (df_corse["durata_minuti"] / 60)).round(2)

# costo stimato
def calcola_costo(riga):
    # calcola costo stimato in base al tipo di corsa e alla durata
    tipo = riga["tipo_corsa"]
    durata = riga["durata_minuti"]
    
    if tipo == "breve":
        return 1.50                                    # tariffa fissa breve
    elif tipo == "media":
        return round(2.50 + 0.10 * (durata - 15), 2)   # base + extra per minuto
    else:
        return round(5.00 + 0.08 * (durata - 45), 2)   # base + extra per minuto
df_corse["costo_stimato"] = df_corse.apply(calcola_costo, axis=1)
print("\nPrime 5 righe con nuove colonne:")
print(df_corse[["id_corsa", "durata_minuti", "tipo_corsa", "velocita_media", "costo_stimato"]].head())

# 6.4 Aggregazione e Merge
print("\n--- 6.4 Aggregazioni ---")

# groupby per città
# raggruppa tuttte le corse per città e calcola più statistiche in una volta
stats_città = df_corse.groupby("città").agg(
    n_corse       = ("id_corsa",       "count"),   # conta le corse
    durata_media  = ("durata_minuti",  "mean"),    # media durata
    km_totali     = ("km_percorsi",    "sum"),     # km totali
    costo_totale  = ("costo_stimato",  "sum"),     # costo totale
).round(2)
 
print("\nStatistiche per città:")
print(stats_città)

# groupby per fascia oraria
stats_fascia = df_corse.groupby("fascia_oraria").agg(
    n_corse         = ("id_corsa",      "count"),
    velocita_media  = ("velocita_media", "mean"),
).round(2)
 
print("\nStatistiche per fascia oraria:")
print(stats_fascia)

# pivot table
# indice = città (righe), colonne = tipo_corsa, valori = numero corse
pivot = df_corse.pivot_table(
    index    = "città",
    columns  = "tipo_corsa",
    values   = "id_corsa",
    aggfunc  = "count", # conta quante corse ci sono per ogni combinazione
    fill_value = 0 # sostituisce i NaN con 0 (celle senza corse)
)
 
print("\nPivot table — corse per città e tipo:")
print(pivot)

# merge: corse + bici + utenti
# primo merge: corse con bici su id_bici
df_merged = pd.merge(df_corse, df_bici, on="id_bici", how="left") # tiene tutte le corse anche se bici non è in df_bici

# secondo merge: aggiungiamo dati utente
df_merged = pd.merge(
    df_merged, df_utenti,
    on       = "id_utente",
    how      = "left",
    # gestisce le colonne con lo stesso nome (es. "città")
    # _x = da df_merged, _y = da df_utenti
    suffixes = ("_corsa", "_utente") 
)
 
print(f"\nDataFrame merged: {df_merged.shape[0]} righe, "
      f"{df_merged.shape[1]} colonne")
print("\nPrime 5 righe (colonne principali):")
print(df_merged[["id_corsa", "id_bici", "tipo", "nome", "tipo_abbonamento", "costo_stimato"]].head())

# Top-N
print("\n--- Top-N ---")

# 5 biciclette con più corse
top_bici = (
    df_corse.groupby("id_bici")["id_corsa"]
    .count()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
    .rename(columns={"id_corsa": "n_corse"})
)
print("\nTop 5 bici per numero di corse:")
print(top_bici)

# 3 utenti Premium con costo totale più alto
top_premium = (
    df_merged[df_merged["tipo_abbonamento"] == "Premium"]
    .groupby(["id_utente", "nome"])["costo_stimato"]
    .sum()
    .sort_values(ascending=False)
    .head(3)
    .reset_index()
    .rename(columns={"costo_stimato": "costo_totale"})
)
print("\nTop 3 utenti Premium per costo totale:")
print(top_premium)

# statistica extra: corse per tipo bici
top_tipo_bici = (
    df_merged.groupby("tipo")["id_corsa"]
    .count()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"id_corsa": "n_corse", "tipo": "tipo_bici"})
)
print("\nCorse per tipo di bici:")
print(top_tipo_bici)

# salvataggio risultati
df_merged.to_csv("output/df_merged.csv", index=False, encoding="utf-8")
stats_città.to_csv("output/stats_città.csv", encoding="utf-8")
pivot.to_csv("output/pivot_corse.csv", encoding="utf-8")
print("\nRisultati salvati in output/")
