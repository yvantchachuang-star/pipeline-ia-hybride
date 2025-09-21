def gen_tests(rôle: str, objectif: str) -> list:
    """
    Génère des scénarios de test fonctionnels et métier pour un rôle et un objectif donné.
    Aligné avec les exigences BABOK.
    """
    tests = []

    # Test métier
    tests.append(f"Vérifier que le {rôle} peut initier l'action : {objectif} depuis son interface métier.")

    # Test fonctionnel
    tests.append(f"Vérifier que la fonctionnalité liée à {objectif} est accessible et opérationnelle pour le {rôle}.")

    # Test de performance
    tests.append(f"Mesurer le temps de réponse de l'action {objectif} pour le {rôle} (objectif : < 2 secondes).")

    # Test de conformité
    tests.append(f"Vérifier que l'action {objectif} respecte les contraintes réglementaires applicables au rôle {rôle}.")

    # Test de qualité
    tests.append(f"Simuler des cas d’usage pour s’assurer que l’action {objectif} fonctionne sans erreur pour le {rôle}.")

    # Test de collaboration
    tests.append(f"Vérifier que le {rôle} peut partager ou transmettre les résultats liés à {objectif} aux autres parties prenantes.")

    return tests
