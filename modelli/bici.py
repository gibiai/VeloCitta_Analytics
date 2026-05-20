# modelli/bici.py
# Gerarchia completa delle classi per VeloCittà Analytics
#
# Struttura:
#   Bicicletta (classe base)
#   ├── BiciclettaClassica  — aggiunge taglia (S/M/L)
#   ├── BiciclettaElettrica — aggiunge batteria, blocca noleggio sotto 20%
#   └── BiciclettaCargo     — aggiunge carico massimo (aggiunta a nostra scelta)
#
#   FlottaBici — gestisce la collezione di biciclette di una città
#
# from __future__ import annotations permette di usare "FlottaBici" come type hint
# dentro la stessa classe prima che sia definita — senza questo Python darebbe errore
from __future__ import annotations

# CLASSE BASE: Bicicletta
class Bicicletta:
    def __init__(
        self, 
        id_bici: str, # es: "MI-042" id unico
        tipo: str, # "classica", "elettrica", "cargo"
        stazione_corrente: str, # stazione dove si trova bici
        km_percorsi: float, # km totale percorsi
        disponibile: bool = True # True default, disponibilità bici
        
    ) -> None: # il costruttore non restituisce nulla
        # attributi pubblici
        self.id_bici = id_bici
        self.tipo = tipo 
        self.stazione_corrente = stazione_corrente
        self.disponibile = disponibile
        # attributi privati
        self._km_percorsi = km_percorsi
        self._utente_corrente = None # inizia a None perchè bici libera
        
        @property
        def km_percorsi(self) -> float:
            # Restituisce km percorsi - solo lettura dall'esterno
            return self._km_percorsi 
        
        def aggiungi_km(self, km: float) -> None:
        # validazione: km deve essere positivo
            if km <= 0:
                raise ValueError(
                    f"I km da aggiungere devono essere positivi, ricevuto: {km}"
                )
            self._km_percorsi += km # aggiungiamo km al valore esistente
            
# NOLEGGIO E RESTITUZIONE
def noleggia(self, utente: str) -> str:
    """
    Segna la bici come in uso dall'utente indicato.
    Aggiorna disponibile e utente_corrente.
    Solleva ValueError se la bici è già in uso.
    """
    if not self.disponibile:
        raise ValueError(
            f"Bici {self.id_bici} già in uso da '{self._utente_corrente}'"
        )
    self.disponibile = False # segna come non disponibile
    self._utente_corrente = utente # salva il nome dell'utente
    return f"Bici {self.id_bici} noleggiata a '{utente}' da {self.stazione_corrente}"

def restituisci(self, stazione: str, km_aggiunta: float) -> None:
    """
    Registra la restituzione della bici.
    Aggiorna la stazione corrente, aggiunge i km percorsi
    e rimette la bici disponibile.
    """
    self.stazione_corrente = stazione          # aggiorna posizione
    self.aggiungi_km(km_aggiunta)              # aggiunge km con validazione
    self.disponibile       = True              # torna disponibile
    self._utente_corrente  = None              # nessun utente corrente
    
# --- Metodi Speciali ---
# __str__  → chiamato da print(bici) e str(bici)
# __repr__ → chiamato nella console interattiva e da repr(bici)  

def __str__(self) -> str:
    stato = "disponibile" if self.disponibile else f"in uso ({self._utente_corrente})"
    return (
        f"[{self.id_bici}] {self.tipo} | "
        f"{self.stazione_corrente} | "
        f"{self._km_percorsi:.1f} km | "
        f"{stato}"
        )
 
def __repr__(self) -> str:
    # Rappresentazione tecnica per debug — mostra tutti i parametri
    return (
        f"Bicicletta(id='{self.id_bici}', tipo='{self.tipo}', "
        f"stazione='{self.stazione_corrente}', km={self._km_percorsi}, "
        f"disponibile={self.disponibile})"
        )
    
# SOTTOCLASSI
# 1 Classica
class BiciclettaClassica(Bicicletta):
    """
    Sottoclasse di Bicicletta per le bici classiche
    Aggiunge l'attributo taglia (S / M / L)
    Eredita TUTTO da Bicicletta: noleggio, restituzione, km ecc
    Override solo di __str__ per includere la taglia
    """
    # attributo di classe
    TAGLIE_VALIDE = ("S", "M", "L")
 
    def __init__(
        self,
        id_bici: str,
        stazione_corrente: str,
        km_percorsi: float,
        taglia: str,                # attributo specifico di questa sottoclasse
        disponibile: bool = True,
    ) -> None:
        super().__init__(id_bici, "classica", stazione_corrente, km_percorsi, disponibile)
        # "in" controlla se un elemento è presente in una sequenza
        if taglia not in self.TAGLIE_VALIDE:
            raise ValueError(
                f"Taglia '{taglia}' non valida. Usa: {self.TAGLIE_VALIDE}"
            )
        self.taglia = taglia   # attributo specifico di BiciclettaClassica
    
    def __str__(self) -> str:
    # Override di __str__ per includere la taglia nella rappresentazione.
        stato = "disponibile" if self.disponibile else f"in uso ({self._utente_corrente})"
        return (
            f"[{self.id_bici}] classica | taglia {self.taglia} | "
            f"{self.stazione_corrente} | "
            f"{self._km_percorsi:.1f} km | "
            f"{stato}"
        )
 
 # 2 Elettrica
class BiciclettaElettrica(Bicicletta):
    """
    Sottoclasse di Bicicletta per le bici elettriche
    Aggiunge batteria_percentuale (0-100)
    Override di noleggia() per bloccare il noleggio sotto 20% di batteria
    Override di __str__ per mostrare il livello batteria
    """
    # soglia minima di batteria per permettere il noleggio
    # attributo di classe — condiviso da tutte le istanze
    BATTERIA_MINIMA_NOLEGGIO = 20
 
    def __init__(
        self,
        id_bici: str,
        stazione_corrente: str,
        km_percorsi: float,
        batteria_percentuale: int,   # 0-100, attributo specifico elettrica
        disponibile: bool = True,
    ) -> None:
        super().__init__(id_bici, "elettrica", stazione_corrente, km_percorsi, disponibile)
        if not 0 <= batteria_percentuale <= 100:
            raise ValueError(
                f"Batteria deve essere tra 0 e 100, ricevuto: {batteria_percentuale}"
            )
        self.batteria_percentuale = batteria_percentuale
 
    def ricarica(self, percentuale: int) -> None:
        """
        Ricarica la batteria della bici elettrica
        Non supera mai il 100% grazie a min()
        min(100, valore) restituisce sempre il più piccolo dei due:
        se valore > 100 restituisce 100, altrimenti restituisce valore
        """
        if percentuale <= 0:
            raise ValueError("La percentuale di ricarica deve essere positiva")
        # min() garantisce che non superiamo mai 100
        # es. 80% + 30% → min(100, 110) → 100%
        self.batteria_percentuale = min(100, self.batteria_percentuale + percentuale)
    
        def noleggia(self, utente: str) -> str:
            """
            Override di noleggia() — aggiunge il controllo batteria.
            Se la batteria è sotto la soglia minima, blocca il noleggio.
            Se è ok, chiama super().noleggia() che fa il resto.
            stessa chiamata bici.noleggia("utente") ma comportamento diverso
            a seconda del tipo reale della bici.
            """
            # controllo specifico per le bici elettriche
            if self.batteria_percentuale < self.BATTERIA_MINIMA_NOLEGGIO:
                raise ValueError(
                    f"Batteria insufficiente ({self.batteria_percentuale}%) — "
                    f"minimo richiesto: {self.BATTERIA_MINIMA_NOLEGGIO}%"
                )
            # se la batteria è ok, delega alla classe base che gestisce il resto
            # super().noleggia() chiama il metodo noleggia() di Bicicletta
            return super().noleggia(utente)
    
        def __str__(self) -> str:
        # Override di __str__ per mostrare il livello batteria
            stato = "disponibile" if self.disponibile else f"in uso ({self._utente_corrente})"
            return (
                f"[{self.id_bici}] elettrica | {self.batteria_percentuale}% | "
                f"{self.stazione_corrente} | "
                f"{self._km_percorsi:.1f} km | "
                f"{stato}"
            )
 
# 3 BiciclettaCargo 
class BiciclettaCargo(Bicicletta):
    """
    Bicicletta cargo per il trasporto merci
    Aggiunge carico_massimo_kg e verifica il peso prima del noleggio
    Dimostra che possiamo aggiungere parametri extra anche a noleggia()
    """
    def __init__(
        self,
        id_bici: str,
        stazione_corrente: str,
        km_percorsi: float,
        carico_massimo_kg: float,   # peso massimo trasportabile in kg
        disponibile: bool = True,
    ) -> None:
 
        super().__init__(id_bici, "cargo", stazione_corrente, km_percorsi, disponibile)
        if carico_massimo_kg <= 0:
            raise ValueError("Il carico massimo deve essere positivo")
        self.carico_massimo_kg = carico_massimo_kg
 
    def noleggia(self, utente: str, peso_carico_kg: float = 0) -> str:
        """
        Override di noleggia() con parametro extra peso_carico_kg.
        peso_carico_kg = 0 è il valore di default — se non specificato assume 0.
        """
        # verifica che il carico richiesto non superi il massimo
        if peso_carico_kg > self.carico_massimo_kg:
            raise ValueError(
                f"Carico {peso_carico_kg} kg supera il massimo "
                f"consentito di {self.carico_massimo_kg} kg"
            )
        return super().noleggia(utente)   # delega il resto alla classe base
    
    def __str__(self) -> str:
        stato = "✓ disponibile" if self.disponibile else f"✗ in uso ({self._utente_corrente})"
        return (
            f"[{self.id_bici}] cargo | max {self.carico_massimo_kg} kg | "
            f"{self.stazione_corrente} | "
            f"{self._km_percorsi:.1f} km | "
            f"{stato}"
        )

# Poliformismo
def stampa_flotta(biciclette: list) -> None:
    """
    Dimostra il polimorfismo: applica la stessa operazione
    a oggetti di tipo diverso senza controllare esplicitamente il tipo
    """ 
    print("\n--- Flotta completa (polimorfismo) ---")
    for bici in biciclette:
        # print(bici) chiama __str__ automaticamente
        # Python decide quale versione usare in base al tipo reale dell'oggetto
        # senza che noi dobbiamo scrivere if type(bici) == BiciclettaClassica: ...
        print(bici)

# Classe Flottabici
class FlottaBici:
    """
    Dataset che gestisce la collezione di biciclette di una città.
    Pattern Dataset: contiene una lista di oggetti e offre metodi
    per aggiungerli, rimuoverli, cercarli e fare statistiche.
    """ 
    def __init__(self, citta: str) -> None:
        self.citta = citta
        # list[Bicicletta] è un type hint avanzato che dice:
        # "questa lista contiene oggetti di tipo Bicicletta (o sue sottoclassi)"
        self.biciclette: list[Bicicletta] = []

    # CRUD: aggiungi, rimuovi, cerca
    def aggiungi(self, bici: Bicicletta) -> None:
        """Aggiunge una bicicletta alla flotta."""
        self.biciclette.append(bici)   # append aggiunge in fondo alla lista
 
    def rimuovi(self, id_bici: str) -> None:
        """
        Rimuove una bicicletta tramite id.
        Usa cerca_per_id() che già solleva KeyError se non trovata.
        """
        bici = self.cerca_per_id(id_bici)   # trova la bici — KeyError se manca
        self.biciclette.remove(bici)         # remove rimuove l'oggetto dalla lista
 
    def cerca_per_id(self, id_bici: str) -> Bicicletta:
        """
        Cerca una bici tramite id e la restituisce.
        Solleva KeyError se non trovata.
        """
        risultati = [b for b in self.biciclette if b.id_bici == id_bici]
        if not risultati:   # lista vuota → nessuna bici trovata
            raise KeyError(f"Bicicletta con id '{id_bici}' non trovata nella flotta")
        return risultati[0]   # [0] prende il primo (e unico) elemento trovato
    
    def disponibili(self) -> list:
        """
        Restituisce la lista delle bici disponibili al noleggio.
        List comprehension con condizione booleana:
        tiene solo le bici dove disponibile == True.
        """
        return [b for b in self.biciclette if b.disponibile]
 
    def statistiche(self) -> dict:
        """
        Calcola statistiche generali sulla flotta.
        Restituisce un dizionario con totale, disponibili, in_uso,
        km_totali_flotta e km_medi_per_bici.
        """
        totale   = len(self.biciclette)             # numero totale bici
        n_disp   = len(self.disponibili())           # numero bici disponibili
        # sum(b.km_percorsi for b in self.biciclette)
        # → somma i km di ogni bici senza creare una lista intermedia
        km_totali = sum(b.km_percorsi for b in self.biciclette)
        # se totale == 0 usiamo 0.0 per evitare divisione per zero
        km_medi   = round(km_totali / totale, 2) if totale > 0 else 0.0
        return {
            "totale":           totale,
            "disponibili":      n_disp,
            "in_uso":           totale - n_disp,    # semplice sottrazione
            "km_totali_flotta": round(km_totali, 2),
            "km_medi_per_bici": km_medi,
        }
        
    @classmethod
    def da_lista(cls, citta: str, dati: list) -> "FlottaBici":
        """
        Costruisce una FlottaBici da una lista di dizionari.
        Ogni dizionario deve avere: id, tipo, stazione, km.
        Chiavi opzionali: taglia (classica), batteria (elettrica), carico_max (cargo).
        cls è la classe stessa — cls(citta) equivale a FlottaBici(citta).
        """
        flotta = cls(citta)   # crea una nuova istanza vuota della classe
 
        for d in dati:
            # scegliamo la sottoclasse giusta in base al campo "tipo"
            if d["tipo"] == "classica":
                bici = BiciclettaClassica(
                    id_bici=d["id"],
                    stazione_corrente=d["stazione"],
                    km_percorsi=d["km"],
                    # .get("taglia", "M") → usa "M" come default se "taglia" non c'è
                    taglia=d.get("taglia", "M"),
                )
            elif d["tipo"] == "elettrica":
                bici = BiciclettaElettrica(
                    id_bici=d["id"],
                    stazione_corrente=d["stazione"],
                    km_percorsi=d["km"],
                    batteria_percentuale=d.get("batteria", 80),
                )
            else:   # cargo o qualsiasi altro tipo
                bici = BiciclettaCargo(
                    id_bici=d["id"],
                    stazione_corrente=d["stazione"],
                    km_percorsi=d["km"],
                    carico_massimo_kg=d.get("carico_max", 50),
                )
            flotta.aggiungi(bici)   # aggiunge la bici appena creata alla flotta
 
        return flotta   # restituisce la flotta completa
    
    # metodi speciali
    def __len__(self) -> int:
        """
        Permette di usare len(flotta) invece di len(flotta.biciclette).
        Python chiama __len__ automaticamente quando scrivi len(oggetto).
        """
        return len(self.biciclette)
 
    def __str__(self) -> str:
        return f"FlottaBici {self.citta} — {len(self)} biciclette"
    

# --- TEST MANUALE ---
 
if __name__ == "__main__":
    print("=" * 50)
    print("TASK 2+3 — OOP VeloCittà")
    print("=" * 50)
 
    # creazione di una bici per ogni tipo
    classica  = BiciclettaClassica("MI-001",  "Cadorna",  120.5, "M")
    elettrica = BiciclettaElettrica("MI-002", "Loreto",    80.0, 75)
    cargo     = BiciclettaCargo("MI-003",     "Centrale",  45.0, 80.0)
 
    # dimostrazione polimorfismo — stessa funzione, oggetti diversi
    stampa_flotta([classica, elettrica, cargo])
 
    # test noleggio
    print("\n--- Noleggio ---")
    print(classica.noleggia("Mario Rossi"))
    print(classica)   # chiama __str__ — mostra ✗ in uso
 
    # test restituzione
    print("\n--- Restituzione ---")
    classica.restituisci("Loreto", 12.3)
    print(classica)   # chiama __str__ — torna ✓ disponibile
 
    # test ValueError batteria bassa
    print("\n--- Test batteria insufficiente ---")
    scarica = BiciclettaElettrica("MI-010", "Duomo", 0.0, 10)  # batteria al 10%
    try:
        scarica.noleggia("Utente")
    except ValueError as e:
        print(f"ValueError: {e}")
 
    # test FlottaBici da lista di dizionari
    print("\n--- FlottaBici.da_lista() ---")
    dati = [
        {"id": "TO-001", "tipo": "classica",  "stazione": "Porta Nuova", "km": 200.0, "taglia": "L"},
        {"id": "TO-002", "tipo": "elettrica", "stazione": "Lingotto",    "km": 150.0, "batteria": 90},
        {"id": "TO-003", "tipo": "cargo",     "stazione": "Porta Nuova", "km": 50.0,  "carico_max": 100},
    ]
    flotta = FlottaBici.da_lista("Torino", dati)
    print(flotta)                        # chiama __str__ di FlottaBici
    print(f"len(flotta): {len(flotta)}") # chiama __len__
 
    print("\n--- Statistiche flotta ---")
    for k, v in flotta.statistiche().items():
        print(f"  {k}: {v}")
 
    print("\n--- Bici disponibili ---")
    for b in flotta.disponibili():
        print(f"  {b}")