from acces_donnees import lister_societes, lire_societe

piege = "' OR '1'='1"

print("Saisie piegee :", piege)
print("lister_societes(piege) ->", lister_societes(piege))
print("lire_societe(piege)    ->", lire_societe(piege))