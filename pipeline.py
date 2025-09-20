# 📦 Typage des exigences selon leur contenu
def typer_exigence(texte):
    texte = texte.lower()
    if any(mot in texte for mot in ["valeur", "efficacité", "objectif", "conformité", "sécurité", "rentabilité", "ponctualité", "fiabilité"]):
        return "Métier"
    elif any(mot in texte for mot in ["interface", "filtrer", "accéder", "gérer", "exporter", "consulter", "rappel", "itinéraire", "notification"]):
        return "Fonctionnelle"
    elif any(mot in texte for mot in ["temps", "performance", "authentification", "pdf", "latence", "chiffrement", "géolocalisation", "push", "sms"]):
        return "Technique"
    elif any(mot in texte for mot in ["client", "gestionnaire", "juriste", "utilisateur", "partenaire", "femme de ménage", "actuaire", "auditeur", "responsable"]):
        return "Partie prenante"
    elif any(mot in texte for mot in ["accessibilité", "ergonomie", "temps de réponse", "robustesse", "responsive", "mode hors ligne"]):
        return "Non fonctionnelle"
    else:
        return "Non classé"

# 🔁 Reformulation du besoin en template structuré
def reformuler_besoin(besoin):
    besoin = besoin.lower()
    if "femme de ménage" in besoin and "arriver à l’heure" in besoin:
        return [
            {
                "acteur": "femme de ménage",
                "action": "recevoir des rappels et des estimations de trajet",
                "objectif": "arriver à l’heure à ses missions"
            },
            {
                "acteur": "responsable planning",
                "action": "suivre les horaires d’arrivée des intervenants",
                "objectif": "anticiper les retards et réorganiser les missions"
            }
        ]
    # Cas par défaut
    return [
        {
            "acteur": "utilisateur",
            "action": f"utiliser le système pour « {besoin} »",
            "objectif": f"atteindre l’objectif « {besoin} »"
        },
        {
            "acteur": "gestionnaire",
            "action": f"faciliter la tâche « {besoin} »",
            "objectif": f"améliorer la productivité"
        },
        {
            "acteur": "analyste",
            "action": f"mesurer l’impact de « {besoin} »",
            "objectif": f"orienter les décisions"
        }
    ]

# 💡 Suggestions IA
def generer_suggestions_ia(template):
    return [
        f"Ajouter une alerte liée à « {template['action']} »",
        f"Définir un indicateur d’efficacité pour « {template['objectif']} »",
        f"Préciser le rôle « {template['acteur']} » : opérationnel ou décisionnel",
        f"Générer une version alternative pour un autre profil métier",
        f"Exporter ce résultat ou l’ajouter au backlog"
    ]

# 🧩 Génération complète d’une user story enrichie
def generer_story_complete(template):
    story = f"En tant que {template['acteur']}, je veux {template['action']} afin de {template['objectif']}."

    exigences_brutes = []

    # Exigences spécifiques selon le rôle
    if template["acteur"] == "femme de ménage":
        exigences_brutes = [
            "L’application affiche les horaires et adresses des missions",
            "Elle envoie une alerte 30 minutes avant le départ",
            "Elle propose un itinéraire optimisé",
            "Géolocalisation pour estimer l’heure d’arrivée",
            "Notifications push ou SMS",
            "Interface simple et accessible sur mobile",
            "Mode hors ligne pour les zones sans réseau"
        ]
    elif template["acteur"] == "responsable planning":
        exigences_brutes = [
            "Visualisation en temps réel de la position des intervenants",
            "Alerte en cas de retard estimé",
            "Possibilité de réassigner une mission",
            "Export des horaires et historiques",
            "Fiabilité du système en cas de réorganisation"
        ]
    else:
        exigences_brutes = [
            f"L’interface permet de {template['action']}",
            f"{template['acteur'].capitalize()} peut accéder à la fonctionnalité « {template['action']} »",
            "L’accès est protégé par une authentification forte",
            "Les données sont exportables en PDF avec horodatage et chiffrement",
            f"{template['acteur'].capitalize()} peut suivre les opérations en temps réel",
            "Le système garantit un temps de réponse inférieur à 2 secondes"
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

# 🧠 Génération des stories à partir du besoin
def generer_stories_depuis_besoin(besoin):
    templates = reformuler_besoin(besoin)
    return [generer_story_complete(t) for t in templates]

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
