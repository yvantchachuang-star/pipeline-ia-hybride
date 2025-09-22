import re

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

def générer_exigences(rôle: str, action: str) -> list:
    return [
        ("Métier", "Objectif métier", f"{rôle.capitalize()} doit pouvoir {action} pour atteindre ses objectifs métier."),
        ("Fonctionnelle", "Fonction clé", f"L'application doit permettre à {rôle} de {action}."),
        ("Non fonctionnel", "Performance attendue", f"La réponse à l'action '{action}' doit être disponible en moins de 2 secondes."),
        ("Informationnelle", "Accès aux données", f"{rôle.capitalize()} doit pouvoir consulter les données liées à '{action}' dans un format structuré."),
        ("Réglementaire", "Conformité", f"L'action '{action}' doit respecter les normes en vigueur dans le secteur."),
        ("Transitionnelle", "Migration ou intégration", f"Les processus existants du rôle {rôle} doivent être migrés sans perte lors de l’introduction de la fonctionnalité '{action}'."),
        ("Qualité", "Fiabilité", f"La fonctionnalité '{action}' doit fonctionner sans erreur dans 99,9% des cas d'utilisation."),
        ("Partie prenante", "Interaction métier", f"{rôle.capitalize()} doit pouvoir collaborer avec les autres profils métier autour de '{action}'.")
    ]

def générer_critères(rôle: str, action: str) -> list:
    return [
        "L'action est réalisable en moins de 3 étapes",
        "Le résultat est visible immédiatement"
    ]

def générer_tests(rôle: str, action: str) -> list:
    return [
        f"Vérifier que le {rôle} peut initier l'action : {action}.",
        f"Vérifier que la fonctionnalité liée à '{action}' est accessible et opérationnelle pour le {rôle}.",
        f"Mesurer le temps de réponse de l'action '{action}' pour le {rôle} (objectif : < 2 secondes).",
        f"Vérifier que l'action '{action}' respecte les contraintes réglementaires applicables au rôle {rôle}.",
        f"Simuler des cas d’usage pour s’assurer que l’action '{action}' fonctionne sans erreur pour le {rôle}.",
        f"Vérifier que le {rôle} peut partager ou transmettre les résultats liés à '{action}' aux autres parties prenantes."
    ]

def générer_suggestions(rôle: str, action: str) -> list:
    return [
        f"Ajouter une option avancée pour le {rôle}",
        "Permettre une personnalisation"
    ]

def générer_validation(rôle: str, action: str) -> str:
    return f"Le {rôle} confirme que l'action '{action}' répond à son besoin métier."

def generer_stories_depuis_besoin(requete: str) -> list:
    rôles_actions = extraire_rôles_et_actions(requete)
    stories = []

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
        stories.append(story)

    return stories

