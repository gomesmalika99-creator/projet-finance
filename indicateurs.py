def _diviser(a, b):
    """Renvoie a / b, ou None si une valeur manque ou si b vaut 0."""
    if a is None or b is None or b == 0:
        return None
    return float(a) / float(b)


def _arrondir(valeur):
    """Arrondit a 2 decimales, ou renvoie None."""
    if valeur is None:
        return None
    return round(valeur, 2)


def marge_nette(resultat_net, chiffre_affaires):
    """Marge nette en pourcentage. Ex : 50 et 1000 donnent 5.0"""
    ratio = _diviser(resultat_net, chiffre_affaires)
    if ratio is None:
        return None
    return _arrondir(ratio * 100)


def liquidite(actifs_courants, passifs_courants):
    """Ex : 150 et 100 donnent 1.5"""
    return _arrondir(_diviser(actifs_courants, passifs_courants))


def endettement(dettes_totales, capitaux_propres):
    """Ex : 300 et 600 donnent 0.5"""
    return _arrondir(_diviser(dettes_totales, capitaux_propres))


def rendement(cours_debut, cours_fin):
    """Rendement en pourcentage. Ex : 100 puis 110 donnent 10.0"""
    if cours_debut is None or cours_fin is None:
        return None
    ratio = _diviser(cours_fin - cours_debut, cours_debut)
    if ratio is None:
        return None
    return _arrondir(ratio * 100)


def moyenne_mobile(cours, fenetre):
    """Ex : [10, 20, 30, 40] sur 2 donnent [10.0, 15.0, 25.0, 35.0]
    None si la liste est vide, si une valeur manque ou si la fenetre est inferieure a 1."""
    if not cours or fenetre is None or fenetre < 1:
        return None
    if any(c is None for c in cours):
        return None
    resultat = []
    for i in range(len(cours)):
        debut = max(0, i - fenetre + 1)
        morceau = cours[debut:i + 1]
        resultat.append(_arrondir(sum(float(c) for c in morceau) / len(morceau)))
    return resultat