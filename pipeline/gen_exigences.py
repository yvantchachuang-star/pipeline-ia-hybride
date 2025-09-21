def gen_exigences(rôle: str, objectif: str) -> list:
    """
    Génère les exigences BABOK enrichies pour un rôle et un objectif donné.
    """
    exigences = [
        # Métier
        ("Métier", "Objectif métier", f"{rôle.capitalize()} doit pouvoir {objectif} pour atteindre ses objectifs métier."),

        # Fonctionnelle
        ("Fonctionnelle", "Fonction clé", f"L'application doit fournir une interface permettant au {rôle} de {objectif}."),

        # Non fonctionnelle
        ("Non fonctionnelle", "Performance attendue", f"La réponse à l'action du {rôle} doit être disponible en moins de 2 secondes."),

        # Informationnelle
        ("Informationnelle", "Accès aux données", f"Le {rôle} doit pouvoir consulter les données liées à {objectif} dans un format structuré."),

        # Réglementaire
        ("Réglementaire", "Conformité", f"L'action du {rôle} liée à {objectif} doit respecter les normes en vigueur dans le secteur."),

        # Transitionnelle
        ("Transitionnelle", "Migration ou intégration", f"Les processus existants du {rôle} doivent être migrés sans perte lors de l’introduction de la fonctionnalité {objectif}."),

        # Qualité
        ("Qualité", "Fiabilité", f"La fonctionnalité liée à {objectif} doit fonctionner sans erreur dans 99,9% des cas d’usage du {rôle}."),

        # Partie prenante
        ("Partie prenante", "Interaction métier", f"Le {rôle} doit pouvoir collaborer avec les autres profils métier autour de {objectif}.")
    ]

    return exigences
