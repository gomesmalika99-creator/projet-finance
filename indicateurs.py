def _diviser(a, b):
    """Renvoie a / b, ou None si b vaut 0 (calcul impossible)."""
    if b is None or b == 0:
        return None
    return a / b


def marge_nette(resultat_net, chiffre_affaires):
    return _diviser(resultat_net, chiffre_affaires)


def liquidite(actifs_courants, passifs_courants):
    return _diviser(actifs_courants, passifs_courants)


def endettement(dettes_totales, capitaux_propres):
    return _diviser(dettes_totales, capitaux_propres)


def rendement(cours_debut, cours_fin):
    """Gain en pourcentage entre deux cours."""
    ratio = _diviser(cours_fin - cours_debut, cours_debut)
    return None if ratio is None else ratio * 100


def moyenne_mobile(cours, fenetre):
    """Liste des moyennes sur 'fenetre' jours. None si la fenetre est impossible."""
    if fenetre <= 0 or fenetre > len(cours):
        return None
    return [sum(cours[i - fenetre:i]) / fenetre for i in range(fenetre, len(cours) + 1)]