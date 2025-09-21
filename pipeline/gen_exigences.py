def gen_exigences(rôle: str, objectif: str) -> list:
    """
    Génère les exigences BABOK pour un rôle et un objectif donné.
    """
    exigences = [
        ("Métier", "Objectif métier", f"{rôle.capitalize()} doit pouvoir {objectif}"),
        ("Fonctionnelle", "Fonction clé", f"Interface permettant au {rôle} de {objectif}")
    ]
    return exigences
