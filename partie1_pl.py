from pulp import *

joueurs = [
    {"nom": "Alice", "score": 88, "salaire": 1200, "poids": 72},
    {"nom": "Bob", "score": 91, "salaire": 1800, "poids": 85},
    {"nom": "Clara", "score": 84, "salaire": 950, "poids": 68},
    {"nom": "David", "score": 93, "salaire": 2100, "poids": 90},
    {"nom": "Emma", "score": 79, "salaire": 800, "poids": 65},
    {"nom": "Frank", "score": 87, "salaire": 2400, "poids": 95},
    {"nom": "Grace", "score": 85, "salaire": 1050, "poids": 70},
    {"nom": "Hugo", "score": 89, "salaire": 1600, "poids": 80},
]

equipes = ["A", "B"]
BUDGET_MAX = 8500
POIDS_MAX_EQUIPE = 250

probleme = LpProblem("Selection_Optimale_Joueurs", LpMaximize)

x = {}
for joueur in joueurs:
    for equipe in equipes:
        x[(joueur["nom"], equipe)] = LpVariable(f"x_{joueur['nom']}_{equipe}", cat=LpBinary)

probleme += lpSum(
    joueur["score"] * (x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")])
    for joueur in joueurs
)

probleme += lpSum(x[(joueur["nom"], "A")] for joueur in joueurs) == 3
probleme += lpSum(x[(joueur["nom"], "B")] for joueur in joueurs) == 3

for joueur in joueurs:
    probleme += x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")] <= 1

probleme += lpSum(
    joueur["salaire"] * (x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")])
    for joueur in joueurs
) <= BUDGET_MAX

probleme += lpSum(
    joueur["poids"] * x[(joueur["nom"], "A")]
    for joueur in joueurs
) <= POIDS_MAX_EQUIPE

probleme += lpSum(
    joueur["poids"] * x[(joueur["nom"], "B")]
    for joueur in joueurs
) <= POIDS_MAX_EQUIPE

probleme.solve()

print("Statut :", LpStatus[probleme.status])

def afficher_equipe(nom_equipe):
    equipe = [joueur for joueur in joueurs if value(x[(joueur["nom"], nom_equipe)]) == 1]

    score_total = sum(j["score"] for j in equipe)
    salaire_total = sum(j["salaire"] for j in equipe)
    poids_total = sum(j["poids"] for j in equipe)

    print(f"\nÉquipe {nom_equipe}")
    print("-" * 30)
    for j in equipe:
        print(f"{j['nom']} | Score: {j['score']} | Salaire: {j['salaire']}$ | Poids: {j['poids']} kg")

    print(f"Score total   : {score_total}")
    print(f"Salaire total : {salaire_total}$")
    print(f"Poids total   : {poids_total} kg")

afficher_equipe("A")
afficher_equipe("B")

joueurs_selectionnes = [
    joueur for joueur in joueurs
    if value(x[(joueur["nom"], "A")]) == 1 or value(x[(joueur["nom"], "B")]) == 1
]

score_global = sum(j["score"] for j in joueurs_selectionnes)
budget_global = sum(j["salaire"] for j in joueurs_selectionnes)

print("\nRésumé global")
print("-" * 30)
print(f"Score total optimal : {score_global}")
print(f"Budget total utilisé: {budget_global}$")