from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class Societe:
    id: int | None
    nom: str
    secteur: str
    devise: str = "EUR"
    symbole: str = ""


@dataclass
class Bilan:
    id: int
    societe_id: int
    annee: int
    chiffre_affaires: Decimal
    resultat_net: Decimal
    actifs_courants: Decimal
    passifs_courants: Decimal
    dettes_totales: Decimal
    capitaux_propres: Decimal


@dataclass
class Cours:
    id: int
    societe_id: int
    date_cours: date
    cloture: Decimal