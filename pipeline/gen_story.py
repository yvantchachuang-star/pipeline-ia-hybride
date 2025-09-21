def gen_objectifs(rôle: str) -> list:
    base = [
        "accéder à une information critique",
        "réaliser une tâche métier efficacement",
        "obtenir une vue consolidée de l’activité",
        "préparer une décision",
        "suivre l’évolution d’un indicateur",
        "valider une opération métier"
    ]
    return [base[(i + hash(rôle)) % len(base)] for i in range(3)]

