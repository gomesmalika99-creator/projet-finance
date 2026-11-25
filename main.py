from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import depot
from schemas import SocieteEntree

app = FastAPI(title="API Client financier")

# Autorise ton front à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def accueil():
    return {"message": "API OK"}


@app.get("/societes")
def get_societes():
    societes = depot.lister_societes()
    return [vars(s) for s in societes]


@app.get("/societes/{id_societe}")
def get_societe(id_societe: int):
    societe = depot.lire_societe(id_societe)
    if societe is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    return vars(societe)


@app.get("/societes/{id_societe}/bilans")
def get_bilans(id_societe: int):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    bilans = depot.lister_bilans(id_societe)
    return [vars(b) for b in bilans]


@app.get("/societes/{id_societe}/cours")
def get_cours(id_societe: int,
              date_debut: date = date(1900, 1, 1),
              date_fin: date = date(2100, 12, 31)):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    cours = depot.lister_cours(id_societe, date_debut, date_fin)
    return [vars(c) for c in cours]


@app.post("/societes", status_code=201)
def post_societe(societe: SocieteEntree):
    nouvelle = depot.ajouter_societe(societe.nom, societe.secteur)
    return vars(nouvelle)