# partie2_glouton.py

from itertools import combinations

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

SCORE_PULP = 524
BUDGET_PULP = 8450
BUDGET_MAX = 8500
POIDS_MAX_EQUIPE = 250
NB_JOUEURS_EQUIPE = 3


def stats_equipe(equipe):
    return {
        "score": sum(j["score"] for j in equipe),
        "salaire": sum(j["salaire"] for j in equipe),
        "poids": sum(j["poids"] for j in equipe),
    }


def afficher_equipe(nom, equipe):
    s = stats_equipe(equipe)
    print(f"\nÉquipe {nom}")
    print("-" * 30)
    for j in equipe:
        print(
            f"{j['nom']} | Score: {j['score']} | "
            f"Salaire: {j['salaire']}$ | Poids: {j['poids']} kg"
        )
    print(f"Score total   : {s['score']}")
    print(f"Salaire total : {s['salaire']}$")
    print(f"Poids total   : {s['poids']} kg")


def solution_complete(equipe_a, equipe_b):
    return len(equipe_a) == NB_JOUEURS_EQUIPE and len(equipe_b) == NB_JOUEURS_EQUIPE


def peut_ajouter(joueur, equipe, salaire_global):
    if len(equipe) >= NB_JOUEURS_EQUIPE:
        return False

    poids_actuel = sum(j["poids"] for j in equipe)
    if poids_actuel + joueur["poids"] > POIDS_MAX_EQUIPE:
        return False

    if salaire_global + joueur["salaire"] > BUDGET_MAX:
        return False

    return True


def construire_equipes(liste_triee):
    equipe_a = []
    equipe_b = []
    salaire_global = 0

    for joueur in liste_triee:
        if peut_ajouter(joueur, equipe_a, salaire_global):
            equipe_a.append(joueur)
            salaire_global += joueur["salaire"]
        elif peut_ajouter(joueur, equipe_b, salaire_global):
            equipe_b.append(joueur)
            salaire_global += joueur["salaire"]

        if solution_complete(equipe_a, equipe_b):
            break

    if not solution_complete(equipe_a, equipe_b):
        return None

    score_total = sum(j["score"] for j in equipe_a + equipe_b)
    budget_total = sum(j["salaire"] for j in equipe_a + equipe_b)

    return {
        "equipe_a": equipe_a,
        "equipe_b": equipe_b,
        "score_total": score_total,
        "budget_total": budget_total,
    }


def normaliser(valeur, vmin, vmax):
    if vmax == vmin:
        return 0
    return (valeur - vmin) / (vmax - vmin)


def equipe_valide(equipe):
    return (
        len(equipe) <= NB_JOUEURS_EQUIPE
        and sum(j["poids"] for j in equipe) <= POIDS_MAX_EQUIPE
    )


def budget_valide(equipe_a, equipe_b):
    total = sum(j["salaire"] for j in equipe_a + equipe_b)
    return total <= BUDGET_MAX


def faisable_restante(equipe_a, equipe_b, restants):
    """
    Vérifie s'il existe au moins une façon de compléter les équipes
    avec les joueurs restants.
    Comme on n'a que 8 joueurs, on peut tester toutes les petites combinaisons.
    """
    manque_a = NB_JOUEURS_EQUIPE - len(equipe_a)
    manque_b = NB_JOUEURS_EQUIPE - len(equipe_b)

    if manque_a < 0 or manque_b < 0:
        return False

    if manque_a + manque_b > len(restants):
        return False

    for combo_a in combinations(restants, manque_a):
        reste_apres_a = [j for j in restants if j not in combo_a]

        for combo_b in combinations(reste_apres_a, manque_b):
            test_a = equipe_a + list(combo_a)
            test_b = equipe_b + list(combo_b)

            if equipe_valide(test_a) and equipe_valide(test_b) and budget_valide(test_a, test_b):
                return True

    return False


def strategie_score_absolu():
    liste_triee = sorted(joueurs, key=lambda j: j["score"], reverse=True)
    return construire_equipes(liste_triee)


def strategie_ratio_score_salaire():
    liste_triee = sorted(
        joueurs,
        key=lambda j: j["score"] / j["salaire"],
        reverse=True
    )
    return construire_equipes(liste_triee)


def strategie_ratio_score_poids():
    liste_triee = sorted(
        joueurs,
        key=lambda j: j["score"] / j["poids"],
        reverse=True
    )
    return construire_equipes(liste_triee)


def strategie_score_normalise_pondere(ws=0.6, wsal=0.25, wp=0.15):
    """
    Stratégie améliorée avec :
    - score pondéré normalisé
    - sélection gloutonne
    - contrôle de faisabilité restante
    """
    scores = [j["score"] for j in joueurs]
    salaires = [j["salaire"] for j in joueurs]
    poids = [j["poids"] for j in joueurs]

    smin, smax = min(scores), max(scores)
    salmin, salmax = min(salaires), max(salaires)
    pmin, pmax = min(poids), max(poids)

    restants = []
    for j in joueurs:
        score_norm = normaliser(j["score"], smin, smax)
        salaire_norm = normaliser(j["salaire"], salmin, salmax)
        poids_norm = normaliser(j["poids"], pmin, pmax)

        valeur = ws * score_norm - wsal * salaire_norm - wp * poids_norm

        jc = j.copy()
        jc["valeur_gloutonne"] = valeur
        restants.append(jc)

    equipe_a = []
    equipe_b = []

    while not solution_complete(equipe_a, equipe_b):
        candidats_tries = sorted(
            restants,
            key=lambda j: j["valeur_gloutonne"],
            reverse=True
        )

        joueur_place = False

        for joueur in candidats_tries:
            essais = []

            salaire_global = sum(j["salaire"] for j in equipe_a + equipe_b)

            if peut_ajouter(joueur, equipe_a, salaire_global):
                essais.append("A")
            if peut_ajouter(joueur, equipe_b, salaire_global):
                essais.append("B")

            for equipe_nom in essais:
                nouvelle_a = equipe_a.copy()
                nouvelle_b = equipe_b.copy()

                if equipe_nom == "A":
                    nouvelle_a.append(joueur)
                else:
                    nouvelle_b.append(joueur)

                nouveaux_restants = [j for j in restants if j["nom"] != joueur["nom"]]

                if faisable_restante(nouvelle_a, nouvelle_b, nouveaux_restants):
                    equipe_a = nouvelle_a
                    equipe_b = nouvelle_b
                    restants = nouveaux_restants
                    joueur_place = True
                    break

            if joueur_place:
                break

        if not joueur_place:
            return None

    score_total = sum(j["score"] for j in equipe_a + equipe_b)
    budget_total = sum(j["salaire"] for j in equipe_a + equipe_b)

    return {
        "equipe_a": equipe_a,
        "equipe_b": equipe_b,
        "score_total": score_total,
        "budget_total": budget_total,
    }


def afficher_resultat(nom_strategie, resultat):
    print("\n" + "=" * 60)
    print(nom_strategie)
    print("=" * 60)

    if resultat is None:
        print("Aucune solution faisable trouvée.")
        return

    afficher_equipe("A", resultat["equipe_a"])
    afficher_equipe("B", resultat["equipe_b"])

    ecart_points = resultat["score_total"] - SCORE_PULP
    ecart_pourcentage = (ecart_points / SCORE_PULP) * 100

    print("\nRésumé global")
    print("-" * 30)
    print(f"Score total   : {resultat['score_total']}")
    print(f"Budget utilisé: {resultat['budget_total']}$")
    print(f"Écart vs PuLP : {ecart_points} pts ({ecart_pourcentage:.2f}%)")


def afficher_tableau_comparatif(resultats):
    print("\n" + "=" * 80)
    print("TABLEAU COMPARATIF")
    print("=" * 80)
    print(
        f"{'Stratégie':35} {'Score total':12} {'Budget utilisé':15} {'Écart vs PuLP':20}"
    )
    print("-" * 80)

    for nom, resultat in resultats.items():
        if resultat is None:
            print(f"{nom:35} {'N/A':12} {'N/A':15} {'Aucune solution':20}")
        else:
            ecart_points = resultat["score_total"] - SCORE_PULP
            ecart_pourcentage = (ecart_points / SCORE_PULP) * 100
            ecart_txt = f"{ecart_points} pts ({ecart_pourcentage:.2f}%)"
            print(
                f"{nom:35}"
                f"{resultat['score_total']:<12}"
                f"{str(resultat['budget_total']) + '$':<15}"
                f"{ecart_txt:<20}"
            )

    print(
        f"{'PuLP (optimal)':35}"
        f"{SCORE_PULP:<12}"
        f"{str(BUDGET_PULP) + '$':<15}"
        f"{'---':<20}"
    )


def main():
    resultats = {
        "Score absolu": strategie_score_absolu(),
        "Ratio score / salaire": strategie_ratio_score_salaire(),
        "Ratio score / poids": strategie_ratio_score_poids(),
        "Score normalisé pondéré": strategie_score_normalise_pondere(),
    }

    for nom, resultat in resultats.items():
        afficher_resultat(nom, resultat)

    afficher_tableau_comparatif(resultats)


if __name__ == "__main__":
    main()