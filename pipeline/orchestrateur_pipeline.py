from pipeline.analyse_roles import analyse_roles
from pipeline.gen_objectifs import gen_objectifs
from pipeline.gen_exigences import gen_exigences
from pipeline.gen_tests import gen_tests
from pipeline.generer_stories_depuis_besoin import (
    generer_critères,
    générer_exigences,
    générer_suggestions,
    générer_validation,
    générer_tests,
    extraire_rôles_et_actions
)

def privatiser_bloc(bloc: dict) -> dict:
    bloc["suggestions"] = ["🔒 Suggestion masquée"]
    bloc["validation"] = "🔒 Validation masquée"
    bloc["exigences"] = [(cat, typ, "🔒 Exigence masquée") for cat, typ, _ in bloc["exigences"]]
    bloc["tests"] = [f"🔒 Test masqué ({i+1})" for i in range(len(bloc["tests"]))]
    return bloc

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
                "exigences": générer_exigences(rôle, action),
                "critères": générer_critères(rôle, action),
                "tests": générer_tests(rôle, action),
                "suggestions": générer_suggestions(rôle, action),
                "validation": générer_validation(rôle, action)
            }
            if privatiser:
                story = privatiser_bloc(story)
            stories.append(story)
        return stories

    # Sinon, fallback sur rôle seul + objectifs générés
    rôles = analyse_roles(requete)
    for rôle in rôles:
        objectifs = gen_objectifs(rôle)
        for obj in objectifs:
            story = {
                "acteur": rôle,
                "action": obj,
                "story": f"En tant que {rôle}, je veux {obj} pour atteindre mes objectifs métier.",
                "exigences": gen_exigences(rôle, obj),
                "critères": [
                    "L'action est réalisable en moins de 3 étapes",
                    "Le résultat est visible immédiatement"
                ],
                "tests": gen_tests(rôle, obj),
                "suggestions": [f"Ajouter une option avancée pour le {rôle}", "Permettre une personnalisation"],
                "validation": f"Le {rôle} confirme que l'action '{obj}' répond à son besoin métier."
            }
            if privatiser:
                story = privatiser_bloc(story)
            stories.append(story)

    return stories
