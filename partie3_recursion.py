# partie3_recursion.py

import time
import matplotlib.pyplot as plt

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

# Tri décroissant par score pour la fonction récursive demandée
joueurs_tries = sorted(joueurs, key=lambda j: j["score"], reverse=True)

# Scores des 2 meilleurs joueurs de la sélection optimale PuLP (Partie 1)
# Solution optimale trouvée : Alice(88), Bob(91), Clara(84), David(93), Emma(79), Hugo(89)
# Les deux meilleurs scores de cette sélection sont donc 93 et 91
FIB_0 = 93
FIB_1 = 91


def score_cumule(joueurs_tries, k):
    """
    Calcule récursivement le score cumulé des k meilleurs joueurs.
    Affiche chaque étape du calcul.
    """
    if k == 0:
        print("score_cumule(joueurs, 0) = 0")
        return 0

    precedent = score_cumule(joueurs_tries, k - 1)
    joueur = joueurs_tries[k - 1]
    resultat = precedent + joueur["score"]

    print(
        f"score_cumule(joueurs, {k}) = "
        f"{precedent} + {joueur['score']} ({joueur['nom']}) = {resultat}"
    )

    return resultat


def fib_naif(n, compteur=None):
    """
    Version naïve récursive de Fibonacci modifié.
    compteur : liste d'un élément pour compter les appels.
    """
    if compteur is not None:
        compteur[0] += 1

    if n == 0:
        return FIB_0
    if n == 1:
        return FIB_1

    return fib_naif(n - 1, compteur) + fib_naif(n - 2, compteur)


def fib_memo(n, memo=None, compteur=None):
    """
    Version mémoïsée de Fibonacci modifié.
    """
    if memo is None:
        memo = {}

    if compteur is not None:
        compteur[0] += 1

    if n in memo:
        return memo[n]

    if n == 0:
        return FIB_0
    if n == 1:
        return FIB_1

    memo[n] = fib_memo(n - 1, memo, compteur) + fib_memo(n - 2, memo, compteur)
    return memo[n]


def graphique_appels_recursifs():
    """
    Graphique du nombre d'appels de fib_naif et fib_memo
    pour n allant de 1 à 25, avec échelle logarithmique.
    """
    valeurs_n = list(range(1, 26))
    appels_naif = []
    appels_memo = []

    for n in valeurs_n:
        compteur_naif = [0]
        compteur_memo = [0]

        fib_naif(n, compteur_naif)
        fib_memo(n, memo={}, compteur=compteur_memo)

        appels_naif.append(compteur_naif[0])
        appels_memo.append(compteur_memo[0])

    plt.figure()
    plt.plot(valeurs_n, appels_naif, label="fib_naif")
    plt.plot(valeurs_n, appels_memo, label="fib_memo")
    plt.yscale("log")
    plt.title("Croissance du nombre d'appels récursifs")
    plt.xlabel("n")
    plt.ylabel("Nombre d'appels (échelle log)")
    plt.legend()
    plt.show()


def main():
    print("=" * 60)
    print("PARTIE 3A - SCORE CUMULÉ RÉCURSIF")
    print("=" * 60)

    k = len(joueurs_tries)
    total = score_cumule(joueurs_tries, k)

    print("\nRésultat final")
    print("-" * 30)
    print(f"Score cumulé des {k} meilleurs joueurs : {total}")

    print("\n" + "=" * 60)
    print("PARTIE 3B - FIBONACCI MODIFIÉ : NAÏF VS MÉMOÏSÉ")
    print("=" * 60)

    n = 35

    debut = time.perf_counter()
    resultat_naif = fib_naif(n)
    fin = time.perf_counter()
    temps_naif = fin - debut

    print(f"fib_naif({n}) = {resultat_naif}   Temps : {temps_naif:.3f} s")

    debut = time.perf_counter()
    resultat_memo = fib_memo(n)
    fin = time.perf_counter()
    temps_memo = fin - debut

    print(f"fib_memo({n}) = {resultat_memo}   Temps : {temps_memo:.6f} s")

    print("\n" + "=" * 60)
    print("GRAPHIQUE - NOMBRE D'APPELS RÉCURSIFS")
    print("=" * 60)

    graphique_appels_recursifs()


if __name__ == "__main__":
    main()