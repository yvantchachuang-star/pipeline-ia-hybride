def gen_story(rôle: str, objectif: str) -> dict:
    """
    Génère une user story complète pour un rôle et un objectif donné, sans exigences.
    """
    story = f"En tant que {rôle}, je veux {objectif} pour atteindre mes objectifs métier."
    critères = ["L'action est réalisable en moins de 3 étapes", "Le résultat est visible immédiatement"]
    tests = [f"Vérifier que le {rôle} peut accéder à la fonctionnalité", "Vérifier que le résultat est conforme"]
    validation = f"Le {rôle} confirme que l'action répond à son besoin métier."
    suggestions = [f"Ajouter une option avancée pour le {rôle}", "Permettre une personnalisation"]

    return {
        "acteur": rôle,
        "story": story,
        "critères": critères,
        "tests": tests,
        "validation": validation,
        "suggestions": suggestions
    }
