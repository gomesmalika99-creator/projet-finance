from indicateurs import marge_nette, liquidite, endettement, rendement, moyenne_mobile

print("=== Exemples du cadrage ===")
print("Marge nette 50 et 1000 :", marge_nette(50, 1000), "(attendu 5.0)")
print("Liquidite 150 et 100   :", liquidite(150, 100), "(attendu 1.5)")
print("Endettement 300 et 600 :", endettement(300, 600), "(attendu 0.5)")
print("Rendement 100 puis 110 :", rendement(100, 110), "(attendu 10.0)")
print("Moyenne mobile [10, 20, 30, 40] sur 2 :", moyenne_mobile([10, 20, 30, 40], 2))
print("   (attendu [10.0, 15.0, 25.0, 35.0])")

print("\n=== Cas limites (attendu None, sans planter) ===")
print("Division par zero      :", marge_nette(50, 0))
print("Valeur absente         :", liquidite(None, 100))
print("Liste vide             :", moyenne_mobile([], 2))
print("Fenetre inferieure a 1 :", moyenne_mobile([10, 20], 0))