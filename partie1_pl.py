from pulp import *
import matplotlib.pyplot as plt

# Données
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
NB_JOUEURS_EQUIPE = 3

# Création du problème
probleme = LpProblem("Selection_Optimale_Joueurs", LpMaximize)

# Variables binaires
x = {}
for joueur in joueurs:
    for equipe in equipes:
        x[(joueur["nom"], equipe)] = LpVariable(
            f"x_{joueur['nom']}_{equipe}",
            cat=LpBinary
        )

# Fonction objectif : maximiser le score total
probleme += lpSum(
    joueur["score"] * (x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")])
    for joueur in joueurs
)

# Contraintes : exactement 3 joueurs par équipe
probleme += lpSum(x[(joueur["nom"], "A")] for joueur in joueurs) == NB_JOUEURS_EQUIPE, "Equipe_A_3_joueurs"
probleme += lpSum(x[(joueur["nom"], "B")] for joueur in joueurs) == NB_JOUEURS_EQUIPE, "Equipe_B_3_joueurs"

# Un joueur ne peut pas appartenir aux deux équipes
for joueur in joueurs:
    probleme += (
        x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")] <= 1,
        f"Unique_{joueur['nom']}"
    )

# Budget total maximum
probleme += lpSum(
    joueur["salaire"] * (x[(joueur["nom"], "A")] + x[(joueur["nom"], "B")])
    for joueur in joueurs
) <= BUDGET_MAX, "Budget_total"

# Poids maximum par équipe
probleme += lpSum(
    joueur["poids"] * x[(joueur["nom"], "A")]
    for joueur in joueurs
) <= POIDS_MAX_EQUIPE, "Poids_max_A"

probleme += lpSum(
    joueur["poids"] * x[(joueur["nom"], "B")]
    for joueur in joueurs
) <= POIDS_MAX_EQUIPE, "Poids_max_B"

# Résolution
probleme.solve()

print("Statut :", LpStatus[probleme.status])


def afficher_equipe(nom_equipe, equipe):
    """Affiche le détail d'une équipe."""
    score_total = sum(j["score"] for j in equipe)
    salaire_total = sum(j["salaire"] for j in equipe)
    poids_total = sum(j["poids"] for j in equipe)

    print(f"\nÉquipe {nom_equipe}")
    print("-" * 30)
    for j in equipe:
        print(
            f"{j['nom']} | Score: {j['score']} | "
            f"Salaire: {j['salaire']}$ | Poids: {j['poids']} kg"
        )

    print(f"Score total   : {score_total}")
    print(f"Salaire total : {salaire_total}$")
    print(f"Poids total   : {poids_total} kg")


def graphique_budget_poids(equipe_a, equipe_b):
    """Affiche un graphique comparant budget et poids des deux équipes."""
    labels = ["Budget", "Poids"]

    budget_a = sum(j["salaire"] for j in equipe_a)
    poids_a = sum(j["poids"] for j in equipe_a)

    budget_b = sum(j["salaire"] for j in equipe_b)
    poids_b = sum(j["poids"] for j in equipe_b)

    x_positions = [0, 1]
    largeur = 0.35

    plt.figure()

    plt.bar(
        [x - largeur / 2 for x in x_positions],
        [budget_a, poids_a],
        largeur,
        label="Équipe A"
    )

    plt.bar(
        [x + largeur / 2 for x in x_positions],
        [budget_b, poids_b],
        largeur,
        label="Équipe B"
    )

    plt.axhline(y=BUDGET_MAX, linestyle="--", label="Budget max")
    plt.axhline(y=POIDS_MAX_EQUIPE, linestyle=":", label="Poids max")

    plt.xticks(x_positions, labels)
    plt.title("Répartition du budget et du poids par équipe")
    plt.legend()
    plt.show()


# Récupération des équipes sélectionnées
equipe_a = [
    joueur for joueur in joueurs
    if value(x[(joueur["nom"], "A")]) == 1
]

equipe_b = [
    joueur for joueur in joueurs
    if value(x[(joueur["nom"], "B")]) == 1
]

# Affichage des équipes
afficher_equipe("A", equipe_a)
afficher_equipe("B", equipe_b)

# Résumé global
joueurs_selectionnes = equipe_a + equipe_b
score_global = sum(j["score"] for j in joueurs_selectionnes)
budget_global = sum(j["salaire"] for j in joueurs_selectionnes)

print("\nRésumé global")
print("-" * 30)
print(f"Score total optimal : {score_global}")
print(f"Budget total utilisé: {budget_global}$")

# Graphique
graphique_budget_poids(equipe_a, equipe_b)