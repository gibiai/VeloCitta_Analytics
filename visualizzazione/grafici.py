# Task 7 — Visualizzazione dati
# Grafico 1 — Serie temporale corse (animato) -> output/01_serie_temporale.png
# Grafico 2 — Distribuzione durate per città  -> output/02_distribuzione_durate.png
# Grafico 3 — Corse per fascia oraria e tipo  -> output/03_fasce_orarie.png
# Grafico 4 — Scatter durata vs velocità      -> output/04_scatter_durata_velocita.png
# Grafico 5 — Dashboard riepilogativa         -> output/05_dashboard.png

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import os
import sys

# aggiungiamo la root del progetto al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# impostazioni globali
# rcParams applica lo stile a tutti i grafici della sessione
plt.rcParams["figure.dpi"]        = 100
plt.rcParams["figure.facecolor"]  = "white"
plt.rcParams["font.size"]         = 11
 
# tema seaborn applicato globalmente
sns.set_theme(style="whitegrid")
 
# cartella output
os.makedirs("output", exist_ok=True)

# caricamento dati
df_corse  = pd.read_csv("output/df_corse_pulito.csv", parse_dates=["data_corsa"])
df_merged = pd.read_csv("output/df_merged.csv",       parse_dates=["data_corsa"])
df_utenti = pd.read_csv("output/df_utenti.csv")

# aggiunge tipo_corsa e costo se non presenti (da pandas_analisi)
if "tipo_corsa" not in df_corse.columns:
    from giorno_1.demo import classifica_corsa
    df_corse["tipo_corsa"] = df_corse["durata_minuti"].apply(classifica_corsa)
 
if "velocita_media" not in df_corse.columns:
    df_corse["velocita_media"] = (
        df_corse["km_percorsi"] / (df_corse["durata_minuti"] / 60)
    ).round(2)
 
print("Dati caricati. Generazione grafici...")

# GRAFICO 1 
# serie temporale corse per città 
# domanda di Business: come varia il numero di corse nel tempo per ogni città?

# raggruppa corse per data e città - conta quante corse per giorno 
serie = (
    df_corse.groupby(["data_corsa", "città"])["id_corsa"]
    .count()
    .reset_index()
    .rename(columns={"id_corsa": "n_corse"})
)

città_lista = serie["città"].unique()
colori      = {"Milano": "#E63946", "Roma": "#457B9D", "Torino": "#2A9D8F"}
date_uniche = sorted(serie["data_corsa"].unique()) 

fig, graf = plt.subplots(figsize=(10, 5))

def aggiorna(frame):
    """
    Funzione chiamata da FuncAnimation ad ogni frame.
    frame va da 0 a len(date_uniche)-1 — indica quante date mostrare.
    Ad ogni frame aggiungiamo una data e ridisegnamo le linee.
    """
    graf.clear() # pulisce il grafico precedente
    # mostriamo solo le date fino al frame corrente
    date_visibili = date_uniche[:frame + 1]
    dati_frame    = serie[serie["data_corsa"].isin(date_visibili)]
 
    for città in città_lista:
        dati_città = dati_frame[dati_frame["città"] == città].sort_values("data_corsa")
        graf.plot(
            dati_città["data_corsa"],
            dati_città["n_corse"],
            marker="o",
            label=città,
            color=colori.get(città, "gray"),
            linewidth=2,
        )
        
    graf.set_title("Corse giornaliere per città", fontsize=13, fontweight="bold")
    graf.set_xlabel("Data")
    graf.set_ylabel("Numero corse")
    graf.legend(loc="upper left")
    graf.set_ylim(0, serie["n_corse"].max() + 5)
    plt.tight_layout()

# anima il grafico chiamando aggiorna() per ogni frame
ani = animation.FuncAnimation(
    fig,
    aggiorna,
    frames=len(date_uniche),
    interval=800,
    repeat=False,
)
# salva l'ultimo frame come PNG statico
aggiorna(len(date_uniche) - 1)
plt.savefig("output/01_serie_temporale.png", bbox_inches="tight")
print("Grafico 1 PNG salvato!")

# salva come GIF animata — richiede pillow (pip install pillow)
# 1 frame al secondo, adatto per le nostre 3 date
ani.save("output/01_serie_temporale.gif", writer="pillow", fps=1)
plt.close()
ani._fig = None   # evita il warning alla chiusura
print("Grafico 1 GIF salvata!")

# GRAFICO 2
# Distribuzione durate per città (Seaborn histplot + KDE)
# Domanda di business: le durate delle corse sono simili tra le città?

fig, graf2 = plt.subplots(figsize=(10, 5))
sns.histplot(
    data    = df_corse,
    x       = "durata_minuti",
    hue     = "città",
    kde     = True,
    alpha   = 0.5,
    ax   = graf2,
)

graf2.set_title("Distribuzione durate corse per città", fontsize=13, fontweight="bold")
graf2.set_xlabel("Durata (minuti)")
graf2.set_ylabel("Numero corse")
plt.tight_layout()
plt.savefig("output/02_distribuzione_durate.png", bbox_inches="tight")
plt.close()
print("Grafico 2 salvato!")

# GRAFICO 3
# Corse per fascia oraria e tipo bici (Seaborn barplot)
# Domanda di business: in quali fasce orarie si usano di più le bici elettriche?

#  aggiunge il tipo bici al DataFrame corse tramite merge
df_corse_tipo = pd.merge(
    df_corse[["id_corsa", "fascia_oraria"]],
    df_merged[["id_corsa", "tipo"]],
    on="id_corsa",
    how="left"
)

# conta le corse per fascia oraria e tipo bici
corse_fascia = (
    df_corse_tipo.groupby(["fascia_oraria", "tipo"])["id_corsa"]
    .count()
    .reset_index()
    .rename(columns={"id_corsa": "n_corse", "tipo": "tipo_bici"})
)
 
fig, graf3 = plt.subplots(figsize=(10, 5))
# barplot con hue -> barre raggruppate per tipo bici dentro ogni fascia oraria
sns.barplot(
    data    = corse_fascia,
    x       = "fascia_oraria",
    y       = "n_corse",
    hue     = "tipo_bici",
    palette = ["#457B9D", "#E63946"],
    ax      = graf3,
)

graf3.set_title("Corse per fascia oraria e tipo bici", fontsize=13, fontweight="bold")
graf3.set_xlabel("Fascia oraria")
graf3.set_ylabel("Numero corse")
graf3.legend(title="Tipo bici")
plt.tight_layout()
plt.savefig("output/03_fasce_orarie.png", bbox_inches="tight")
plt.close()
print("Grafico 3 salvato!")

# GRAFICO 4
# Scatter durata vs velocità con linea di tendenza
# Domanda di business: le corse più lunghe sono anche più veloci o più lente?

fig, graf4 = plt.subplots(figsize=(10, 5))
# un colore per città 
colori_città = {"Milano": "#E63946", "Roma": "#457B9D", "Torino": "#2A9D8F"}
for città, gruppo in df_corse.groupby("città"):
    graf4.scatter(
        gruppo["durata_minuti"],
        gruppo["velocita_media"],
        label   = città,
        color   = colori_città.get(città, "gray"),
        alpha   = 0.6,
        s       = 60,     # dimensione punti
    )

# linea di tendenza
# polyfit(x, y, 1) → regressione lineare (grado 1 = retta)
# restituisce i coefficienti [m, q] della retta y = mx + q
x = df_corse["durata_minuti"].values
y = df_corse["velocita_media"].values
m, q        = np.polyfit(x, y, 1)         # coefficienti della retta
x_linea     = np.linspace(x.min(), x.max(), 100)  # 100 punti sull'asse x
y_linea     = m * x_linea + q             # valori y corrispondenti
 
graf4.plot(x_linea, y_linea, color="black", linewidth=1.5,
        linestyle="--", label="Tendenza")

graf4.set_title("Durata vs Velocità media per città", fontsize=13, fontweight="bold")
graf4.set_xlabel("Durata (minuti)")
graf4.set_ylabel("Velocità media (km/h)")
graf4.legend()
plt.tight_layout()
plt.savefig("output/04_scatter_durata_velocita.png", bbox_inches="tight")
plt.close()
print("Grafico 4 salvato!")

# GRAFICO 5
# Dashboard riepilogativa (2x2 subplots)
# Domanda di business: panoramica generale delle performance di VeloCittà

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Dashboard VeloCittà Analytics", fontsize=16, fontweight="bold")

# bar chart corse per città: in alto a sx
corse_per_città = df_corse.groupby("città")["id_corsa"].count()
 
axes[0, 0].bar(
    corse_per_città.index,
    corse_per_città.values,
    color=["#E63946", "#457B9D", "#2A9D8F"]
)
axes[0, 0].set_title("Corse per città")
axes[0, 0].set_xlabel("Città")
axes[0, 0].set_ylabel("Numero corse")

# alto a dx: pie chart abbonamenti utenti
abbonamenti = df_utenti["tipo_abbonamento"].value_counts()
 
axes[0, 1].pie(
    abbonamenti.values,
    labels    = abbonamenti.index,
    autopct   = "%1.1f%%",   # mostra la percentuale su ogni fetta
    colors    = ["#E63946", "#457B9D", "#2A9D8F"],
    startangle= 90,
)
axes[0, 1].set_title("Distribuzione abbonamenti utenti")

# basso a sX: bar chart costo totale per città
# prima cerca la colonna nel DataFrame mergiata - in caso si chiami diversamente
col_città = "città_corsa" if "città_corsa" in df_merged.columns else "città"
costo_città = df_merged.groupby(col_città)["costo_stimato"].sum()
 
axes[1, 0].bar(
    costo_città.index,
    costo_città.values,
    color=["#E63946", "#457B9D", "#2A9D8F"]
)
axes[1, 0].set_title("Costo totale stimato per città (€)")
axes[1, 0].set_xlabel("Città")
axes[1, 0].set_ylabel("€")

# in basso a dx: boxplot durate per tipo di corsa
# boxplot mostra mediana, quartili e outlier per ogni categoria
sns.boxplot(
    data    = df_corse,
    x       = "tipo_corsa",
    y       = "durata_minuti",
    hue     = "tipo_corsa",
    palette = {"breve": "#2A9D8F", "media": "#457B9D", "lunga": "#E63946"},
    order   = ["breve", "media", "lunga"],
    legend  = False,
    ax      = axes[1, 1],
)
axes[1, 1].set_title("Distribuzione durate per tipo corsa")
axes[1, 1].set_xlabel("Tipo corsa")
axes[1, 1].set_ylabel("Durata (minuti)")
 
plt.tight_layout()
plt.savefig("output/05_dashboard.png", bbox_inches="tight")
plt.close()
print("Grafico 5 salvato!")

# print finale
print("\nTutti i grafici salvati in output/")
