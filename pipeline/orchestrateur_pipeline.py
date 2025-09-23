import re
from pipeline.analyse_roles import analyse_roles
from pipeline.gen_objectifs import gen_objectifs
from pipeline.gen_exigences import gen_exigences
from pipeline.gen_tests import gen_tests

# 🔍 Extraction rôle + action depuis la requête
def extraire_rôles_et_actions(requete: str) -> list:
    rôles_actions = []
    phrases = re.split(r"[.]", requete)
    for phrase in phrases:
        match = re.search(r"(le|la|l’|un|une)?\s*(\w+)\s+(veut|souhaite|désire|demande)\s+(.*)", phrase.strip(), re.IGNORECASE)
        if match:
            rôle = match.group(2).lower()
            action = match.group(4).strip()
            rôles_actions.append((rôle, action))
    return rôles_actions

# 🔐 Masquage des livrables sensibles
def privatiser_bloc(bloc: dict) -> dict:
    bloc["suggestions"] = ["🔒 Suggestion masquée"]
    bloc["validation"] = "🔒 Validation masquée"
    bloc["exigences"] = [(cat, typ, "🔒 Exigence masquée") for cat, typ, _ in bloc["exigences"]]
    bloc["tests"] = [f"🔒 Test masqué ({i+1})" for i in range(len(bloc["tests"]))]
    return bloc

# ✅ Critères d’acceptation standards
def générer_critères(rôle: str, action: str) -> list:
    return [
        "L'action est réalisable en moins de 3 étapes",
        "Le résultat est visible immédiatement"
    ]

# 💡 Suggestions IA
def générer_suggestions(rôle: str, action: str) -> list:
    return [
        f"Ajouter une option avancée pour le {rôle}",
        "Permettre une personnalisation"
    ]

# 🔒 Validation métier
def générer_validation(rôle: str, action: str) -> str:
    return f"Le {rôle} confirme que l'action '{action}' répond à son besoin métier."

# 🧠 Orchestration principale
def orchestrer_pipeline(requete: str, privatiser: bool = False) -> list:
    rôles_actions = extraire_rôles_et_actions(requete)
    stories = []

    if rôles_actions:
        # Format rôle + action détecté
        for rôle, action in rôles_actions:
            story = {
                "acteur": rôle,
                "action": action,
                "story": f"En tant que {rôle}, je veux {action} pour atteindre mes objectifs métier.",
                "exigences": gen_exigences(rôle, action),
                "critères": générer_critères(rôle, action),
                "tests": gen_tests(rôle, action),
                "suggestions": générer_suggestions(rôle, action),
                "validation": générer_validation(rôle, action)
            }
            if privatiser:
                story = privatiser_bloc(story)
            stories.append(story)
        return stories

    # Sinon, fallback sur rôle seul + 1 objectif généré
    rôles = analyse_roles(requete)
    for rôle in rôles:
        objectifs = gen_objectifs(rôle)
        if objectifs:
            obj = objectifs[0]
            story = {
                "acteur": rôle,
                "action": obj,
                "story": f"En tant que {rôle}, je veux {obj} pour atteindre mes objectifs métier.",
                "exigences": gen_exigences(rôle, obj),
                "critères": générer_critères(rôle, obj),
                "tests": gen_tests(rôle, obj),
                "suggestions": générer_suggestions(rôle, obj),
                "validation": générer_validation(rôle, obj)
            }
            if privatiser:
                story = privatiser_bloc(story)
            stories.append(story)

    return stories
