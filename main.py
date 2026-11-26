import logging
from datetime import date

import pymysql
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import depot
from schemas import SocieteEntree

logger = logging.getLogger("api")

app = FastAPI(
    title="API Client financier",
    description="API REST qui expose les sociétés, leurs bilans et leurs cours de clôture.",
    version="1.0.0",
)

# Autorise ton front à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Le front web est servi à l'adresse http://127.0.0.1:8000/app/
app.mount("/app", StaticFiles(directory="frontend", html=True), name="front")

# Codes d'erreur affichés dans /docs
R_404 = {404: {"description": "Société introuvable"}}
R_409 = {409: {"description": "La demande contredit l'état de la base"}}
R_422 = {422: {"description": "Données invalides (type, longueur ou champ manquant)"}}


@app.get("/", tags=["Accueil"], summary="Vérifier que l'API répond")
def accueil():
    return {"message": "API OK"}


@app.get("/societes", tags=["Sociétés"], summary="Lister les sociétés",
         description="Renvoie toutes les sociétés, triées par nom.")
def get_societes():
    societes = depot.lister_societes()
    return [vars(s) for s in societes]


@app.get("/societes/{id_societe}", tags=["Sociétés"], summary="Lire une société",
         description="Renvoie une société à partir de son identifiant.",
         responses={**R_404, **R_422})
def get_societe(id_societe: int):
    societe = depot.lire_societe(id_societe)
    if societe is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    return vars(societe)


@app.post("/societes", status_code=201, tags=["Sociétés"], summary="Créer une société",
          description="Crée une société. Le nom (1 à 100 caractères) et le secteur "
                      "(1 à 50 caractères) sont obligatoires.",
          responses={**R_409, **R_422})
def post_societe(societe: SocieteEntree):
    nouvelle = depot.ajouter_societe(societe.nom, societe.secteur)
    return vars(nouvelle)


@app.put("/societes/{id_societe}", tags=["Sociétés"], summary="Remplacer une société",
         description="Remplace le nom et le secteur d'une société existante.",
         responses={**R_404, **R_409, **R_422})
def put_societe(id_societe: int, societe: SocieteEntree):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    depot.remplacer_societe(id_societe, societe.nom, societe.secteur)
    return vars(depot.lire_societe(id_societe))


@app.delete("/societes/{id_societe}", status_code=204, tags=["Sociétés"],
            summary="Supprimer une société",
            description="Supprime une société. Refusé (409) si elle a encore des bilans.",
            responses={**R_404, **R_409, **R_422})
def delete_societe(id_societe: int):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    if depot.compter_bilans(id_societe) > 0:
        raise HTTPException(status_code=409,
                            detail="Suppression impossible : la société a encore des bilans")
    depot.supprimer_societe(id_societe)


@app.get("/societes/{id_societe}/bilans", tags=["Bilans et cours"],
         summary="Lister les bilans d'une société",
         description="Renvoie les bilans annuels d'une société, triés par année.",
         responses={**R_404, **R_422})
def get_bilans(id_societe: int):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    bilans = depot.lister_bilans(id_societe)
    return [vars(b) for b in bilans]


@app.get("/societes/{id_societe}/cours", tags=["Bilans et cours"],
         summary="Lister les cours de clôture d'une société",
         description="Renvoie les cours de clôture. On peut filtrer avec "
                     "date_debut et date_fin (format AAAA-MM-JJ).",
         responses={**R_404, **R_422})
def get_cours(id_societe: int,
              date_debut: date = date(1900, 1, 1),
              date_fin: date = date(2100, 12, 31)):
    if depot.lire_societe(id_societe) is None:
        raise HTTPException(status_code=404, detail="Société introuvable")
    cours = depot.lister_cours(id_societe, date_debut, date_fin)
    return [vars(c) for c in cours]


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