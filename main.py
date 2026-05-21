# MAIN - Entry Point del progetto
# esegue tutti i moduli in ordine corretto

import subprocess
import sys
import os
 
def esegui(script: str, descrizione: str) -> bool:
    """Esegue uno script Python e restituisce True se va a buon fine."""
    print(f"\n{'=' * 40}")
    print(f"  {descrizione}")
    print(f"{'-' * 40}")
    # subprocess.run esegue lo script come processo separato
    # sys.executable usa lo stesso Python con cui è stato lanciato main.py
    risultato = subprocess.run(
        [sys.executable, script],
        capture_output=False,   # mostra l'output direttamente nel terminale
    )
    if risultato.returncode != 0:
        print(f"\nERRORE IN {script} - processo interrotto!")
        return False
    print(f"\n{descrizione} completato.")
    return True

if __name__ == "__main__":
    # spostiamo la cartella di lavoro alla directory dove si trova main.py
    # così tutti i percorsi relativi (analisi/, output/ ecc.) funzionano
    # indipendentemente da dove lanci il comando nel terminale
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("\n" + "█" * 55)
    print("  VeloCittà Analytics — Avvio progetto")
    print("█" * 55)
    # crea cartella output se non esite
    os.makedirs("output", exist_ok=True)
    
    # sequenza di esecuzione - ordine importante:
    # demo.py non va eseguito da qui (è solo una libreria di funzioni)
    # l'ordine garantisce che ogni script trovi i file che gli servono
    passi = [
        ("analisi/numpy_analisi.py",   "Task 5 — Analisi NumPy"),
        ("analisi/pandas_pulizia.py",  "Task 6.1-6.2 — Pandas: creazione e pulizia"),
        ("analisi/pandas_analisi.py",  "Task 6.3-6.4 — Pandas: analisi e aggregazioni"),
        ("visualizzazione/grafici.py", "Task 7 — Visualizzazione grafici"),
    ]
    for script, descrizione in passi:
        ok = esegui(script, descrizione)
        if not ok:
            sys.exit(1)   # interrompe se uno script fallisce
            
    print("\n" + "█" * 55)
    print("  Tutti i task completati con successo!")
    print("  Grafici salvati in: output/")
    print("█" * 55 + "\n")