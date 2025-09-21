def reformuler_question(message: str) -> str | None:
    msg = message.lower().strip()

    if "je veux comprendre" in msg or "explique" in msg:
        return "Souhaitez-vous que je vous présente les exigences métier ou les tests associés à un rôle spécifique ?"
    if "je ne comprends pas" in msg or "c'est quoi" in msg or "définis" in msg:
        return "Souhaitez-vous une définition d’un type d’exigence BABOK ou d’un livrable métier ?"
    if "comment ça marche" in msg or "comment fonctionne" in msg:
        return "Souhaitez-vous que je vous décrive le fonctionnement d’un rôle métier ou d’un processus métier ?"
    if "je veux voir les rôles" in msg or "montre les rôles" in msg:
        return "Souhaitez-vous que je vous liste les rôles métier extraits de la requête initiale ?"
    if "je veux les tests" in msg or "montre les tests" in msg:
        return "Souhaitez-vous que je vous affiche les scénarios de test pour un rôle ou une exigence spécifique ?"
    if "je veux les exigences" in msg or "montre les exigences" in msg:
        return "Souhaitez-vous que je vous affiche les exigences BABOK pour un rôle donné ?"

    return None
