# Task 1.2 — Funzioni di utilità per VeloCittà Analytics
# File contiene 3 funzioni che vengono usate da tutto il progetto
# calcolo_durata_minuti: converte orari in una durata in minuti
# classifica_corsa: categorizza una corsa in breve / media / lunga
# riepilogo_corse: calcola statistiche su una lista di durate

def calcola_durata_minuti(ora_inizio: str, ora_fine: str) -> int:
    # Step 1: separare ore e minuti dalla stringa
    # map applica int() a ogni elemento lista
    # try/except cattura due errori: se str non convertibile int
    # e se lo split non produce due parti es ("0830") senza ":"
    try:
        ore_inizio,   minuti_inizio = map(int, ora_inizio.split(":"))
        ore_fine,     minuti_fine   = map(int, ora_fine.split(":"))
    except (ValueError, IndexError):
        raise ValueError("Formato orario non valido. Usa 'HH:MM' (es. '08:30')")
    
    # Step 2: validare che i valori siano orari reali
    # senza questo controllo "99:99" passerebbe la conversione in int
    # ma non è un orario valido
    # 0 <= x <= 23 verifica ore, 0 <= x <= 59 verifica minuti
    if not (0 <= ore_inizio <= 23 and 0 <= minuti_inizio <= 59):
        raise ValueError(f"ora_inizio '{ora_inizio}' non è un orario valido")
 
    if not (0 <= ore_fine <= 23 and 0 <= minuti_fine <= 59):
        raise ValueError(f"ora_fine '{ora_fine}' non è un orario valido")
    
    # Step 3: convertire tutto in minuti totali dalla 00:00
    # Per confronto migliore converto tutto in unico numero
    # Esempio: 08:30 → 8 * 60 + 30 = 510 minuti dalla mezzanotte
    #          09:15 → 9 * 60 + 15 = 555 minuti dalla mezzanotte
    totale_inizio = ore_inizio * 60 + minuti_inizio # es. 8 * 60 + 30 = 510
    totale_fine = ore_fine * 60 + minuti_fine
    
    # Step 4: validazione ordine
    # Se ora_fine è prima di ora_inizio calcolo non ha senso
    if totale_fine < totale_inizio:
        raise ValueError(
            f"ora_fine '{ora_fine}' è precedente a ora_inizio '{ora_inizio}'"
        )
    
    # Step 5: calcolo e restituzione
    # semplice sottrazione: 555 - 510 = 45 minuti
    # return riporta il risultato
    return totale_fine - totale_inizio

def classifica_corsa(durata_minuti: int) -> str:
    if durata_minuti < 15:
        return "breve" # meno di 15 min -> breve
    elif durata_minuti <= 45:
        return "media" # tra 15 e 45 min inclusi -> media
    else:
        return "lunga" # tutto il resto (> 45 min) -> lunga
    
def riepilogo_corse(lista_durate: list) -> dict:
    # Se lista vuota non possiamo calcolare media, max, min → errore
    if not lista_durate:
        raise ValueError("la lista delle durate non può essere vuota!")
    
    classificazioni = [classifica_corsa(d) for d in lista_durate] # classificazione di ogni corsa
    return {
        # numero totale di corse
        "totale": len(lista_durate),
        # media aritmetica
        "media": round(sum(lista_durate) / len(lista_durate), 2),
        # durata massima
        "max": max(lista_durate),
        # durata minima
        "min": min(lista_durate),
        # quante corse brevi
        "brevi": classificazioni.count("breve"),
        # quante corse medie
        "medie": classificazioni.count("media"),
        # quante corse lunghe
        "lunghe": classificazioni.count("lunga")
    }
    
# --------------- Test Manuale --------------  
# eseguito SOLO SE lanciato direttamente: python3 demo.py

if __name__ == "__main__":    
# test calcola_durata_minuti
# Verifica il calcolo corretto della durata in minuti tra due orari validi
    print("\n--- calcola_durata_minuti ---")
    print(f"08:00 -> 08:30 = {calcola_durata_minuti('08:00', '08:30')} min") # atteso: 30
    print(f"07:15 → 08:00 = {calcola_durata_minuti('07:15', '08:00')} min")   # atteso: 45
    print(f"10:00 → 11:30 = {calcola_durata_minuti('10:00', '11:30')} min")   # atteso: 90

# test edge case: corsa di durata zero
# Verifica che il formato senza ":" venga rifiutato con ValueError
    print("\n--- Test ValueError (formato non valido) ---")
    try:
        calcola_durata_minuti("0830", "0900") # manca il ":"
    except ValueError as e:
        print(f"ValueError catturato correttamente: {e}")

# test ValueError: orario non valido
# Verifica che ore o minuti fuori range (es. 99:99) vengano rifiutati
    print("\n--- test ValueError (orario non valido) ---")
    try:
        calcola_durata_minuti("99:99", "10:00")
    except ValueError as e:
        print(f"ValueError catturato correttamente: {e}")
    
# test classifica_corsa
# Verifica la classificazione corretta ai confini delle fasce (15 e 45 min)
    print("\n--- classifica_corsa ---")
    for minuti in [10, 15, 30, 45, 60]:
        print(f"  {minuti:>3} min → {classifica_corsa(minuti)}")

# test riepilogo_corse
# Verifica che il riepilogo calcoli tutte le statistiche e i conteggi per tipo
    print("\n--- riepilogo_corse ---")
    durate_esempio = [10, 20, 30, 50, 8, 45, 60, 15, 5, 35]
    print(f"  Input: {durate_esempio}")
    riepilogo = riepilogo_corse(durate_esempio)
    for chiave, valore in riepilogo.items():
        print(f"  {chiave}: {valore}")
        
# test ValueError: lista vuota
# Verifica che una lista vuota sollevi ValueError invece di crashare
    print("\n--- test ValueError (lista vuota) ---")
    try:
        riepilogo_corse([])
    except ValueError as e:
        print(f"ValueError catturato correttamente: {e}")