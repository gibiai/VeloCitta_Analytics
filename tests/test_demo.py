# Test automatici per le funzioni di giorno_1/demo.py
# Ogni test usa assert — se la condizione è False il test fallisce

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from giorno_1.demo import calcola_durata_minuti, classifica_corsa, riepilogo_corse

def test_calcola_durata_minuti():
    # caso base
    assert calcola_durata_minuti("08:00", "08:30") == 30
    assert calcola_durata_minuti("07:15", "08:00") == 45
    assert calcola_durata_minuti("10:00", "11:30") == 90
    # durata zero — stesso orario
    assert calcola_durata_minuti("09:00", "09:00") == 0
    print("✓ calcola_durata_minuti — OK")

def test_calcola_durata_minuti_errori():
    # ora_fine prima di ora_inizio -> ValueError
    try:
        calcola_durata_minuti("10:00", "09:00")
        assert False, "Doveva sollevare ValueError"
    except ValueError:
        pass

    # formato non valido -> ValueError
    try:
        calcola_durata_minuti("0830", "0900")
        assert False, "Doveva sollevare ValueError"
    except ValueError:
        pass

    # orario non valido -> ValueError
    try:
        calcola_durata_minuti("99:99", "10:00")
        assert False, "Doveva sollevare ValueError"
    except ValueError:
        pass

    print("calcola_durata_minuti errori — OK")

def test_classifica_corsa():
    # breve: < 15 min
    assert classifica_corsa(1)  == "breve"
    assert classifica_corsa(14) == "breve"
    # media: 15-45 min inclusi
    assert classifica_corsa(15) == "media"
    assert classifica_corsa(30) == "media"
    assert classifica_corsa(45) == "media"
    # lunga: > 45 min
    assert classifica_corsa(46) == "lunga"
    assert classifica_corsa(90) == "lunga"
    print("classifica_corsa — OK")

def test_riepilogo_corse():
    durate = [10, 20, 30, 50, 8, 45, 60, 15, 5, 35]
    r = riepilogo_corse(durate)

    assert r["totale"] == 10
    assert r["max"]    == 60
    assert r["min"]    == 5
    assert r["brevi"]  == 3   # 10, 8, 5
    assert r["medie"]  == 5   # 20, 30, 45, 15, 35
    assert r["lunghe"] == 2   # 50, 60
    print("riepilogo_corse — OK")

def test_riepilogo_corse_lista_vuota():
    try:
        riepilogo_corse([])
        assert False, "Doveva sollevare ValueError"
    except ValueError:
        pass
    print("riepilogo_corse lista vuota — OK")

if __name__ == "__main__":
    print("=" * 40)
    print("Test demo.py")
    print("=" * 40)

    test_calcola_durata_minuti()
    test_calcola_durata_minuti_errori()
    test_classifica_corsa()
    test_riepilogo_corse()
    test_riepilogo_corse_lista_vuota()

    print("\nTutti i test passati!")