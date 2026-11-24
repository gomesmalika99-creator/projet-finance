from datetime import date
from acces_donnees import lire_societe, lister_bilans, lister_cours
from indicateurs import marge_nette, liquidite, endettement, rendement, moyenne_mobile

ID_SOCIETE = 1
FENETRE = 3


def afficher(nom, valeur, pourcentage=False):
    if valeur is None:
        print(f"  {nom:<12}: calcul impossible (division par zero)")
    elif pourcentage:
        print(f"  {nom:<12}: {valeur:.2f} %")
    else:
        print(f"  {nom:<12}: {valeur:.2f}")


def main():
    societe = lire_societe(ID_SOCIETE)
    if societe is None:
        print("Societe introuvable. Lancez d'abord : python charger_jeu_de_test.py")
        return

    print(f"=== {societe.nom} ===")
    print(f"Secteur : {societe.secteur} | Devise : {societe.devise}")

    bilans = lister_bilans(societe.id)
    if bilans:
        b = bilans[-1]
        print(f"\nIndicateurs de l'annee {b.annee} :")
        marge = marge_nette(b.resultat_net, b.chiffre_affaires)
        afficher("Marge nette", None if marge is None else marge * 100, pourcentage=True)
        afficher("Liquidite", liquidite(b.actifs_courants, b.passifs_courants))
        afficher("Endettement", endettement(b.dettes_totales, b.capitaux_propres))

    cours = lister_cours(societe.id, date(2024, 12, 1), date(2024, 12, 31))
    clotures = [c.cloture for c in cours]
    if len(clotures) >= 2:
        afficher("Rendement", rendement(clotures[0], clotures[-1]), pourcentage=True)

    print(f"\nMoyenne mobile sur {FENETRE} jours :")
    moyennes = moyenne_mobile(clotures, FENETRE)
    if moyennes is None:
        print("  calcul impossible (pas assez de cours)")
    else:
        for c, m in zip(cours[FENETRE - 1:], moyennes):
            print(f"  {c.date_cours} : {m:.2f}")


if __name__ == "__main__":
    main()