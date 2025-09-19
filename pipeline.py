def typer_exigence(texte):
    texte = texte.lower()
    if any(mot in texte for mot in ["valeur", "efficacité", "objectif", "conformité", "rentabilité"]):
        return "Métier"
    elif any(mot in texte for mot in ["interface", "action", "fonction", "affichage", "filtrer", "exporter"]):
        return "Fonctionnelle"
    elif any(mot in texte for mot in ["temps", "performance", "sécurité", "latence", "format", "pdf"]):
        return "Technique"
    elif any(mot in texte for mot in ["client", "gestionnaire", "utilisateur", "comptable", "partenaire"]):
        return "Partie prenante"
    elif any(mot in texte for mot in ["accessibilité", "ergonomie", "temps de réponse", "robustesse", "fiabilité"]):
        return "Non fonctionnelle"
    else:
        return "Non classé"

def generer_suggestions_ia(template):
    return [
        f"Ajouter une règle de gestion liée à « {template['action']} »",
        f"Définir un indicateur de performance pour « {template['objectif']} »",
        f"Préciser le rôle « {template['acteur']} » : opérationnel ou stratégique",
        f"Générer une version alternative pour un autre acteur",
        f"Exporter ce résultat ou l’ajouter au backlog"
    ]

def generer_story_complete(template):
    story = f"En tant que {template['acteur']}, je veux {template['action']} afin de {template['objectif']}."

    exigences_brutes = [
        f"Les factures sont accessibles depuis l’interface de gestion",
        f"Le tri par date et client permet de {template['objectif']}",
        f"Les données sont exportables en PDF avec un format standardisé",
        f"{template['acteur'].capitalize()} peut filtrer par client ou montant",
        f"Le temps de chargement des factures ne dépasse pas 2 secondes"
    ]

    exigences_typées = [(typer_exigence(e), e) for e in exigences_brutes]

    critères = exigences_brutes[:3]
    tests = [
        f"Accéder à l’interface liée à {template['action']}",
        f"Exécuter l’action : {template['action']}",
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

def generer_stories_depuis_besoin(besoin):
    besoin = besoin.lower()
    stories = []

    if "facture" in besoin:
        stories.append({
            "acteur": "gestionnaire",
            "action": "consulter les factures en temps réel",
            "objectif": "suivre les paiements efficacement"
        })
        stories.append({
            "acteur": "comptable",
            "action": "exporter les factures au format PDF",
            "objectif": "préparer les audits financiers"
        })
        stories.append({
            "acteur": "client",
            "action": "accéder à mes factures depuis mon espace personnel",
            "objectif": "vérifier mes dépenses"
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
