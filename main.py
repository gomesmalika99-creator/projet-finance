import logging
from datetime import date

import pymysql
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import depot
from schemas import SocieteEntree

logger = logging.getLogger("api")

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


@app.put("/societes/{id_societe}")
def put_societe(id_societe: int, societe: SocieteEntree):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    depot.remplacer_societe(id_societe, societe.nom, societe.secteur)
    return vars(depot.lire_societe(id_societe))


@app.delete("/societes/{id_societe}", status_code=204)
def delete_societe(id_societe: int):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    if depot.compter_bilans(id_societe) > 0:
        raise HTTPException(status_code=409,
                            detail="Suppression impossible : la société a encore des bilans")
    depot.supprimer_societe(id_societe)


# ===== Gestion des erreurs =====
@app.exception_handler(pymysql.err.IntegrityError)
def erreur_integrite(request: Request, exc: Exception):
    # La base refuse la demande (contrainte) : 409, sans détail technique
    return JSONResponse(status_code=409,
                        content={"detail": "La demande contredit l'état de la base"})


@app.exception_handler(Exception)
def erreur_imprevue(request: Request, exc: Exception):
    # Le détail reste dans le terminal, jamais dans la réponse
    logger.exception("Erreur imprévue")
    return JSONResponse(status_code=500,
                        content={"detail": "Erreur interne du serveur"})