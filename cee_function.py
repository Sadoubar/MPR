# cee_functions.py
import math

# --- Constantes et Données ---
SEUILS = {
    "idf": {
        1: [23768, 28933, 40404],
        2: [34884, 42463, 59394],
        3: [41893, 51000, 71060],
        4: [48914, 59549, 83637],
        5: [55961, 68123, 95758],
        "supplémentaire": [7038, 8568, 12122]
    },
    "hors_idf": {
        1: [17173, 22015, 30844],
        2: [25115, 32197, 45340],
        3: [30206, 38719, 54592],
        4: [35285, 45234, 63844],
        5: [40388, 51775, 73098],
        "supplémentaire": [5094, 6525, 9254]
    }
}

IDF_DEPARTEMENTS = {"75", "77", "78", "91", "92", "93", "94", "95"}

PLAFONDS_TRAVAUX = {
    "gain_2_classes": 40000,
    "gain_3_classes": 55000,
    "gain_4_classes_ou_plus": 70000
}

TAUX_FINANCEMENT = {
    "très_modestes": {"gain_2_classes": 0.80, "gain_3_classes": 0.80, "gain_4_classes_ou_plus": 0.80},
    "modestes": {"gain_2_classes": 0.60, "gain_3_classes": 0.60, "gain_4_classes_ou_plus": 0.60},
    "intermédiaires": {"gain_2_classes": 0.45, "gain_3_classes": 0.50, "gain_4_classes_ou_plus": 0.50},
    "supérieurs": {"gain_2_classes": 0.10, "gain_3_classes": 0.15, "gain_4_classes_ou_plus": 0.20}
}

BONUS_SORTIE_PASSOIRE = 0.10

TAUX_ECRETEMENT = {
    "très_modestes": 1.00,
    "modestes": 0.80,
    "intermédiaires": 0.80,
    "supérieurs": 0.50
}

PRISE_EN_CHARGE_MAR = {
    "très_modestes": 1.00,
    "modestes": 0.80,
    "intermédiaires": 0.40,
    "supérieurs": 0.20
}

PLAFOND_MAR = 2000
PLAFOND_MAR_HABITAT_INDIGNE = 4000

CLASSES_ORDRE = ["G", "F", "E", "D", "C", "B", "A"]
CLASSES_ORDRE_INV = {classe: i for i, classe in enumerate(CLASSES_ORDRE)}


# --- Fonctions de Calcul ---

def verifier_region(code_postal):
    """Vérifie si le code postal correspond à l'Île-de-France ou non."""
    if not code_postal or not code_postal.isdigit() or len(code_postal) != 5:
        return None
    return "idf" if code_postal[:2] in IDF_DEPARTEMENTS else "hors_idf"


def determiner_categorie(code_postal, personnes, revenu):
    """Détermine la catégorie de ressources du ménage."""
    region = verifier_region(code_postal)
    if not region:
        return None, "Code postal invalide.", None, None

    if not isinstance(personnes, int) or personnes < 1:
        return None, "Nombre de personnes invalide.", None, None

    if not isinstance(revenu, (int, float)) or revenu < 0:
        return None, "Revenu fiscal invalide.", None, None

    seuils_region = SEUILS[region]

    if personnes <= 5:
        seuils_perso = seuils_region.get(personnes)
    else:
        base = seuils_region[5]
        supp = seuils_region["supplémentaire"]
        seuils_perso = [(base[i] + supp[i] * (personnes - 5)) for i in range(3)]

    if not seuils_perso:
        return None, "Erreur interne de calcul des seuils.", None, None

    if revenu <= seuils_perso[0]:
        cat, cat_d = "très_modestes", "revenus très modestes"
    elif revenu <= seuils_perso[1]:
        cat, cat_d = "modestes", "revenus modestes"
    elif revenu <= seuils_perso[2]:
        cat, cat_d = "intermédiaires", "revenus intermédiaires"
    else:
        cat, cat_d = "supérieurs", "revenus supérieurs"

    # Retourne la catégorie, la description, la région et les seuils
    return cat, f"Ménage aux {cat_d}", region, seuils_perso


def calculer_aide_maprimereno(categorie, gain_reel, cout_travaux_ht, cout_travaux_ttc, est_passoire_energetique):
    """Calcule l'aide MaPrimeRénov' en fonction des paramètres fournis."""
    if not isinstance(gain_reel, int) or gain_reel < 2:
        return None

    # Déterminer le type de gain
    if gain_reel == 2:
        type_gain = "gain_2_classes"
    elif gain_reel == 3:
        type_gain = "gain_3_classes"
    else:
        type_gain = "gain_4_classes_ou_plus"

    # Calcul de l'aide
    plafond = PLAFONDS_TRAVAUX.get(type_gain, 0)
    taux_base = TAUX_FINANCEMENT.get(categorie, {}).get(type_gain, 0)
    taux_final = taux_base + BONUS_SORTIE_PASSOIRE if est_passoire_energetique else taux_base
    cout_eligible_ht = min(cout_travaux_ht, plafond)
    aide_brute = cout_eligible_ht * taux_final

    # Écrêtement
    taux_ecret = TAUX_ECRETEMENT.get(categorie, 0)
    montant_max_aide_ttc = cout_travaux_ttc * taux_ecret
    aide_nette_mpr = min(aide_brute, montant_max_aide_ttc)
    ecretement_applique = aide_brute > aide_nette_mpr

    # Calcul de l'aide à l'accompagnement (MAR)
    taux_mar_pct = PRISE_EN_CHARGE_MAR.get(categorie, 0) * 100
    aide_mar_base = round(min(PLAFOND_MAR * (taux_mar_pct / 100), PLAFOND_MAR), 2)

    # Reste à charge
    reste_a_charge_mpr = round(cout_travaux_ttc - aide_nette_mpr, 2)

    # Retourner les résultats détaillés
    return {
        "plafond_travaux": plafond,
        "taux_base": taux_base * 100,
        "taux_avec_bonus": taux_final * 100,
        "bonus_applique": est_passoire_energetique,
        "taux_ecretement": taux_ecret * 100,
        "cout_eligible_ht": round(cout_eligible_ht, 2),
        "aide_base": round(aide_brute, 2),
        "montant_max_aide": round(montant_max_aide_ttc, 2),
        "aide_finale": round(aide_nette_mpr, 2),
        "aide_mar_base": aide_mar_base,
        "taux_mar": taux_mar_pct,
        "reste_a_charge": reste_a_charge_mpr,
        "ecretement_applique": ecretement_applique
    }


def valider_performance(classe_actuelle, classe_apres):
    """Valide si le gain de performance énergétique est conforme aux exigences."""
    if classe_actuelle not in CLASSES_ORDRE_INV or classe_apres not in CLASSES_ORDRE_INV:
        return False, 0, "Classes énergétiques invalides."

    index_actuel = CLASSES_ORDRE_INV[classe_actuelle]
    index_apres = CLASSES_ORDRE_INV[classe_apres]

    # Calcul du gain en nombre de classes
    gain_reel = index_apres - index_actuel

    if gain_reel <= 0:
        return False, gain_reel, "La classe visée doit être meilleure que la classe actuelle."
    if gain_reel < 2:
        return False, gain_reel, f"Gain insuffisant ({gain_reel} classe(s)). Il faut au moins 2 classes pour MPR Ampleur."

    # Vérification des exigences de classe finale minimale
    if classe_actuelle in ["F", "G"] and index_apres < CLASSES_ORDRE_INV["C"]:
        return False, gain_reel, f"Classe visée ({classe_apres}) trop basse : minimum C requis si départ {classe_actuelle}."
    elif classe_actuelle == "E" and index_apres < CLASSES_ORDRE_INV["B"]:
        return False, gain_reel, f"Classe visée ({classe_apres}) trop basse : minimum B requis si départ E."

    return True, gain_reel, f"Gain de {gain_reel} classes et classe finale {classe_apres} valides."