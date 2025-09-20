import re

# 🔍 Détection automatique du rôle dans un bloc
def extraire_partie_prenante(texte):
    texte = texte.lower().strip()
    if "en tant que" in texte:
        match = re.search(r"en tant que\s+([a-zàéèêç\- ]+)", texte)
        if match:
            return match.group(1).strip()
    elif "veut" in texte:
        return texte.split("veut")[0].replace("le ", "").replace("la ", "").replace("l'", "").strip()
    return "utilisateur"

# 🔁 Reformulation naturelle du besoin
def reformuler_besoin(besoin):
    besoin = besoin.strip()
    acteur = extraire_partie_prenante(besoin)

    outil = "solution"
    match = re.search(r"veut\s+(?:un|une|des)?\s*(\w+)?\s*(.*)", besoin.lower())
    if match:
        outil = match.group(1) or "solution"
        reste = match.group(2).strip()
        verbe_match = re.search(r"(d’|de\s+)?([a-zéèêàç\- ]+)", reste)
        if verbe_match:
            verbe_phrase = verbe_match.group(2).strip()
            action = f"recevoir une {outil} qui permet de {verbe_phrase}"
            objectif = verbe_phrase[0].upper() + verbe_phrase[1:]
        else:
            action = f"utiliser une {outil} adaptée à son besoin"
            objectif = "atteindre son objectif métier"
    else:
        action = f"utiliser une {outil} adaptée"
        objectif = "répondre à son besoin métier"

    return [
        {
            "acteur": acteur,
            "action": action,
            "objectif": objectif
        },
        {
            "acteur": acteur,
            "action": f"améliorer ses pratiques grâce à une {outil} dédiée",
            "objectif": f"Optimiser ses résultats liés à {objectif.lower()}"
        },
        {
            "acteur": acteur,
            "action": f"tester et ajuster ses méthodes avec une {outil} intelligente",
            "objectif": f"Obtenir une qualité constante dans {objectif.lower()}"
        }
    ]

# 🧠 Segmentation multi-acteurs
def segmenter_requete(requete):
    segments = re.split(r"\s+et\s+|\s*,\s*", requete)
    blocs = []
    for segment in segments:
        match = re.search(r"(le|la|l’|les)?\s*([a-zàéèêç\- ]+?)\s+veut\s+(.*)", segment.lower())
        if match:
            acteur = match.group(2).strip()
            besoin = match.group(3).strip()
            blocs.append(f"Le {acteur} veut {besoin}")
    return blocs

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

# 🧠 Génération des stories multi-acteurs
def generer_stories_depuis_besoin(requete):
    blocs = segmenter_requete(requete)
    all_stories = []
    for bloc in blocs:
        templates = reformuler_besoin(bloc)
        stories = [generer_story_complete(t) for t in templates]
        all_stories.extend(stories)
    return all_stories

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

    md += "\n\n# 📘 Définition des types d’exigences\n"
    md += "- **Métier** : Objectifs ou besoins exprimés par l’organisation (valeur, efficacité, conformité)\n"
    md += "- **Fonctionnelle** : Comportement attendu du système (actions, interfaces, règles)\n"
    md += "- **Technique** : Contraintes d’architecture, performance, sécurité, formats\n"
    md += "- **Partie prenante** : Besoins spécifiques d’un acteur (client, gestionnaire, partenaire)\n"
    md += "- **Non fonctionnelle** : Qualités du système (temps de réponse, accessibilité, robustesse, ergonomie)\n"

    return md
