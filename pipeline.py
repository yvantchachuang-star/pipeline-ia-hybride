import re

def extraire_roles_depuis_requete(requete):
    # Extraction dynamique des rôles via "En tant que X"
    matches = re.findall(r"en tant que (\w+)", requete.lower())
    return list(set(matches)) or ["utilisateur"]

def generer_stories_depuis_besoin(requete):
    rôles = extraire_roles_depuis_requete(requete)
    stories = []

    for rôle in rôles:
        objectif = f"réaliser une action clé liée à {rôle}"
        story = f"En tant que {rôle}, je veux {objectif} pour atteindre mes objectifs métier."
        critères = [f"L'action est réalisable en moins de 3 étapes", f"Le résultat est visible immédiatement"]
        tests = [f"Vérifier que le {rôle} peut accéder à la fonctionnalité", f"Vérifier que le résultat est conforme"]
        validation = f"Le {rôle} confirme que l'action répond à son besoin métier."
        suggestions = [f"Ajouter une option avancée pour le {rôle}", f"Permettre une personnalisation"]
        exigences = [
            ("Métier", "Objectif métier", f"{rôle.capitalize()} doit pouvoir {objectif}"),
            ("Fonctionnelle", "Fonction clé", f"Interface permettant au {rôle} de {objectif}")
        ]
        babok = f"Exigence métier identifiée pour le rôle {rôle}, liée à l'objectif : {objectif}."

        stories.append({
            "acteur": rôle,
            "story": story,
            "critères": critères,
            "tests": tests,
            "validation": validation,
            "suggestions": suggestions,
            "babok": babok,
            "exigences": exigences
        })

    return stories

def repondre_chat(message, stories):
    message = message.lower()
    réponses = []

    for s in stories:
        if any(mot in message for mot in s["story"].lower().split()):
            réponses.append(f"🧩 **User Story** : {s['story']}\n📘 **Exigences associées** :")
            for typ, babok, texte in s["exigences"]:
                réponses.append(f"- **{typ}** : {texte} *(BABOK : {babok})*")

    if réponses:
        return "\n\n".join(réponses)
    else:
        return "🤖 Je peux t’aider à explorer les exigences, clarifier un besoin ou proposer une amélioration. Pose-moi une question liée aux rôles, aux livrables ou aux processus métier."
