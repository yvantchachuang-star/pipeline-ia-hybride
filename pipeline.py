import re

def extraire_roles_depuis_requete(requete):
    # Détection dynamique des rôles via "le X", "la X", "en tant que X"
    candidats = re.findall(r"\ble (\w+)", requete.lower()) + \
                re.findall(r"\bla (\w+)", requete.lower()) + \
                re.findall(r"\ben tant que (\w+)", requete.lower())
    return list(set(candidats)) or ["utilisateur"]

def generer_stories_depuis_besoin(requete):
    rôles = extraire_roles_depuis_requete(requete)
    stories = []
    objectifs = [
        "accéder à une information critique",
        "réaliser une tâche métier efficacement",
        "obtenir une vue consolidée de l’activité",
        "préparer une décision",
        "suivre l’évolution d’un indicateur",
        "valider une opération métier"
    ]

    for rôle in rôles:
        for i in range(3):
            objectif = objectifs[(i + hash(rôle)) % len(objectifs)]
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
        match_story = message in s["story"].lower()
        match_role = message in s["acteur"]
        match_exigences = any(message in texte.lower() or message in babok.lower() or message in typ.lower()
                              for typ, babok, texte in s["exigences"])
        match_tests = any(message in t.lower() for t in s["tests"])
        match_critères = any(message in c.lower() for c in s["critères"])
        match_suggestions = any(message in sug.lower() for sug in s["suggestions"])

        if match_story or match_role or match_exigences or match_tests or match_critères or match_suggestions:
            réponses.append(f"🧩 **User Story** : {s['story']}")
            réponses.append("📘 **Exigences associées** :")
            for typ, babok, texte in s["exigences"]:
                réponses.append(f"- **{typ}** : {texte} *(BABOK : {babok})*)")
            réponses.append("✅ **Critères d’acceptation** :")
            for c in s["critères"]:
                réponses.append(f"- {c}")
            réponses.append("🧪 **Tests fonctionnels** :")
            for t in s["tests"]:
                réponses.append(f"- {t}")
            réponses.append("💡 **Suggestions IA** :")
            for sug in s["suggestions"]:
                réponses.append(f"- {sug}")
            réponses.append("🔒 **Validation métier** :")
            réponses.append(s["validation"])
            réponses.append("")

    if réponses:
        return "\n".join(réponses)
    else:
        return "🤖 Je n’ai pas trouvé d’élément correspondant. Essaie avec un rôle métier, un type d’exigence ou un mot-clé métier."
