# 📦 Typage des exigences selon leur contenu
def typer_exigence(texte):
    texte = texte.lower()
    if any(mot in texte for mot in ["valeur", "efficacité", "objectif", "conformité", "rentabilité", "sécurisé"]):
        return "Métier"
    elif any(mot in texte for mot in ["interface", "action", "fonction", "affichage", "filtrer", "exporter", "accéder"]):
        return "Fonctionnelle"
    elif any(mot in texte for mot in ["temps", "performance", "sécurité", "latence", "format", "pdf", "authentification"]):
        return "Technique"
    elif any(mot in texte for mot in ["client", "gestionnaire", "utilisateur", "comptable", "juriste", "partenaire"]):
        return "Partie prenante"
    elif any(mot in texte for mot in ["accessibilité", "ergonomie", "temps de réponse", "robustesse", "fiabilité"]):
        return "Non fonctionnelle"
    else:
        return "Non classé"

# 💡 Suggestions IA interactives
def generer_suggestions_ia(template):
    return [
        f"Ajouter une règle de sécurité liée à « {template['action']} »",
        f"Définir un indicateur d’efficacité pour « {template['objectif']} »",
        f"Préciser le rôle « {template['acteur']} » : opérationnel ou décisionnel",
        f"Générer une version alternative pour un autre profil métier",
        f"Exporter ce résultat ou l’ajouter au backlog"
    ]

# 🧩 Génération complète d’une user story enrichie
def generer_story_complete(template):
    story = f"En tant que {template['acteur']}, je veux {template['action']} afin de {template['objectif']}."

    exigences_brutes = [
        f"L’interface permet de filtrer les contrats par client, date et statut",
        f"L’accès aux contrats est protégé par une authentification forte",
        f"Les contrats sont exportables en PDF avec signature et horodatage",
        f"{template['acteur'].capitalize()} peut suivre les échéances contractuelles",
        f"Le système garantit un temps de réponse inférieur à 2 secondes"
    ]

    exigences_typées = [(typer_exigence(e), e) for e in exigences_brutes]

    critères = exigences_brutes[:3]
    tests = [
        f"Se connecter avec un compte {template['acteur']}",
        f"Accéder à la fonctionnalité : {template['action']}",
        f"Vérifier le résultat attendu lié à {template['objectif']}"
    ]
    validation = f"Le besoin métier « {template['objectif']} » est couvert par la fonctionnalité « {template['action']} »."
    suggestions = generer_suggestions_ia(template)

    return {
        "story": story,
        "exigences": exigences_typées,
        "critères": critères,
        "tests": tests,
        "validation": validation,
        "suggestions": suggestions
    }

# 🧠 Génération de 3 user stories à partir d’un besoin métier
def generer_stories_depuis_besoin(besoin):
    besoin = besoin.lower()
    stories = []

    if "contrat" in besoin:
        stories.append({
            "acteur": "gestionnaire",
            "action": "accéder aux contrats en ligne de manière sécurisée",
            "objectif": "suivre les échéances et engagements"
        })
        stories.append({
            "acteur": "juriste",
            "action": "valider les clauses sensibles des contrats",
            "objectif": "garantir la conformité juridique"
        })
        stories.append({
            "acteur": "client",
            "action": "consulter mes contrats depuis mon espace personnel",
            "objectif": "vérifier mes engagements"
        })
    else:
        stories.append({
            "acteur": "utilisateur",
            "action": f"réaliser l’action liée à « {besoin} »",
            "objectif": f"atteindre l’objectif « {besoin} »"
        })
        stories.append({
            "acteur": "gestionnaire",
            "action": f"faciliter la tâche « {besoin} »",
            "objectif": f"améliorer la productivité"
        })
        stories.append({
            "acteur": "analyste",
            "action": f"mesurer l’impact de « {besoin} »",
            "objectif": f"orienter les décisions"
        })

    return [generer_story_complete(s) for s in stories]

# 📥 Format Markdown pour export
def formater_markdown(stories, exigences_globales):
    md = "# 📘 Exigences classées par type\n"
    types = ["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"]
    for t in types:
        md += f"\n## 🟦 {t}\n"
        for typ, texte in exigences_globales:
            if typ == t:
                md += f"- {texte}\n"

    for i, s in enumerate(stories, start=1):
        md += f"\n# 🧩 Story {i}\n"
        md += f"**User Story**\n{s['story']}\n\n"
        md += "## ✅ Critères d’acceptation\n"
        for c in s["critères"]:
            md += f"- {c}\n"
        md += "\n## 🧪 Tests fonctionnels\n"
        for t in s["tests"]:
            md += f"- {t}\n"
        md += f"\n## 🔒 Validation métier\n{s['validation']}\n"
        md += "\n## 💡 Suggestions IA\n"
        for sug in s["suggestions"]:
            md += f"- {sug}\n"

    md += """
# 📘 Définition des types d’exigences

- **Métier** : Objectifs ou besoins exprimés par l’organisation (valeur, efficacité, conformité)  
- **Fonctionnelle** : Comportement attendu du système (actions, interfaces, règles)  
- **Technique** : Contraintes d’architecture, performance, sécurité, formats  
- **Partie prenante** : Besoins spécifiques d’un acteur (client, gestionnaire, partenaire)  
- **Non fonctionnelle** : Qualités du système (temps de réponse, accessibilité, robustesse, ergonomie)
"""
    return md

# ✅ Vérification locale
if __name__ == "__main__":
    besoin_test = "Un système de gestion des contrats sécurisé et efficace"
    stories = generer_stories_depuis_besoin(besoin_test)
    exigences = []
    for s in stories:
        exigences.extend(s["exigences"])
    markdown = formater_markdown(stories, exigences)
    print("✅ pipeline.py fonctionne correctement")
    print(markdown[:500])
