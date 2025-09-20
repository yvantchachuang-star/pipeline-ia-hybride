import re

# 🔍 Détection automatique du rôle dans la requête
def extraire_partie_prenante(texte):
    texte = texte.lower().strip()
    if "en tant que" in texte:
        return texte.split("en tant que")[1].split("je veux")[0].strip()
    elif "veut" in texte:
        return texte.split("veut")[0].replace("le ", "").replace("la ", "").replace("l'", "").strip()
    return "utilisateur"

# 🔁 Reformulation du besoin en template structuré
def reformuler_besoin(besoin):
    besoin = besoin.strip()
    besoin_lower = besoin.lower()
    acteur = extraire_partie_prenante(besoin)

    match = re.search(r"veut (un|une|des)?\s*(\w+)?\s*(.*)", besoin_lower)
    if match:
        outil = match.group(2) or "système"
        reste = match.group(3).strip()
        action = f"utiliser {outil} pour {reste}"
        objectif = reste[0].upper() + reste[1:] if reste else "atteindre son objectif métier"
        return [{
            "acteur": acteur,
            "action": action,
            "objectif": objectif
        }]
    else:
        return [{
            "acteur": acteur,
            "action": f"utiliser un système pour répondre à son besoin",
            "objectif": f"atteindre son objectif métier"
        }]

# 📦 Typage adaptatif des exigences
def typer_exigence(texte):
    texte = texte.lower().strip()

    if texte.startswith("le besoin métier") or "objectif" in texte or "valeur" in texte or "résultat attendu" in texte:
        return "Métier"
    if any(texte.startswith(prefix) for prefix in [
        "l’interface permet de", "l’application permet de", "le système permet de",
        "permet de", "affiche", "envoie", "propose", "autorise", "gère", "filtre"
    ]):
        return "Fonctionnelle"
    if any(tech in texte for tech in [
        "géolocalisation", "pdf", "chiffrement", "authentification", "temps de réponse",
        "algorithme", "base de données", "intégration", "api", "latence", "performance"
    ]):
        return "Technique"
    if texte.startswith("en tant que") or "peut accéder" in texte or "avec un compte" in texte:
        return "Partie prenante"
    if any(qualité in texte for qualité in [
        "ergonomie", "accessibilité", "mode hors ligne", "interface mobile",
        "temps de chargement", "responsive", "robustesse", "utilisable en conduite"
    ]):
        return "Non fonctionnelle"
    return "Non classé"

# 💡 Suggestions IA
def generer_suggestions_ia(template):
    return [
        f"Ajouter une alerte liée à « {template['action']} »",
        f"Définir un indicateur d’efficacité pour « {template['objectif']} »",
        f"Proposer une version alternative pour un autre profil métier",
        f"Exporter ce résultat ou l’ajouter au backlog"
    ]

# 🧩 Génération complète d’une user story enrichie
def generer_story_complete(template):
    story = f"En tant que {template['acteur']}, je veux {template['action']} afin de {template['objectif']}."

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
