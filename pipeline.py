import re

# 🔍 Détection automatique du rôle
def extraire_partie_prenante(texte):
    texte = texte.lower().strip()
    match = re.search(r"(le|la|l’|les)?\s*([a-zàéèêç\- ]+?)\s+(veut|souhaite|voudrait|demande|attend|a besoin de|recherche)", texte)
    if match:
        return match.group(2).strip()
    match_implicite = re.search(r"pour\s+(le|la|l’|les)?\s*([a-zàéèêç\- ]+)", texte)
    if match_implicite:
        return match_implicite.group(2).strip()
    return "utilisateur"

# 🧠 Segmentation multi-acteurs avec syntaxe libre
def segmenter_requete(requete):
    segments = re.split(r"\s+et\s+|\s*,\s*", requete)
    blocs = []
    for segment in segments:
        segment = segment.strip().lower()
        match = re.search(r"(le|la|l’|les)?\s*([a-zàéèêç\- ]+?)\s+(veut|souhaite|voudrait|demande|attend|a besoin de|recherche)\s+(.*)", segment)
        if match:
            acteur = match.group(2).strip()
            besoin = match.group(4).strip()
            blocs.append(f"Le {acteur} veut {besoin}")
        else:
            match_implicite = re.search(r"(.*)\s+(pour|du côté|chez)\s+(le|la|l’|les)?\s*([a-zàéèêç\- ]+)", segment)
            if match_implicite:
                besoin = match_implicite.group(1).strip()
                acteur = match_implicite.group(4).strip()
                blocs.append(f"Le {acteur} veut {besoin}")
    return blocs

# 🔁 Reformulation fluide et non redondante
def reformuler_besoin(besoin):
    besoin = besoin.strip()
    acteur = extraire_partie_prenante(besoin)
    match = re.search(r"veut\s+(.*)", besoin.lower())
    contenu = match.group(1).strip() if match else besoin
    contenu = re.sub(r"^(un|une|des|le|la|les)\s+", "", contenu)
    contenu = contenu.rstrip(".")
    objectif = contenu.capitalize()

    return [
        {"acteur": acteur, "action": f"accéder rapidement à {contenu}", "objectif": objectif},
        {"acteur": acteur, "action": f"améliorer ses pratiques autour de {contenu}", "objectif": f"Optimiser les résultats liés à {contenu}"},
        {"acteur": acteur, "action": f"ajuster ses méthodes concernant {contenu}", "objectif": f"Obtenir une qualité constante dans {contenu}"}
    ]

# 📦 Typage adaptatif + BABOK
def typer_exigence(texte):
    texte = texte.lower().strip()
    if "objectif" in texte or "valeur" in texte or "résultat attendu" in texte:
        return ("Métier", "Exigence métier")
    if any(texte.startswith(prefix) for prefix in ["l’interface permet de", "le système permet de", "permet de", "affiche", "envoie", "gère"]):
        return ("Fonctionnelle", "Exigence fonctionnelle")
    if any(tech in texte for tech in ["pdf", "chiffrement", "authentification", "temps de réponse", "api", "performance"]):
        return ("Technique", "Exigence non fonctionnelle")
    if "peut accéder" in texte or "avec un compte" in texte:
        return ("Partie prenante", "Exigence des parties prenantes")
    if any(q in texte for q in ["ergonomie", "responsive", "mode hors ligne", "accessibilité"]):
        return ("Non fonctionnelle", "Exigence non fonctionnelle")
    return ("Non classé", "Non classé")

# 💡 Suggestions IA alignées BABOK
def generer_suggestions_ia(template):
    return [
        f"Identifier les règles métier liées à « {template['action']} »",
        f"Valider si l’exigence est stratégique ou opérationnelle",
        f"Cartographier les capacités organisationnelles nécessaires",
        f"Aligner cette exigence avec les objectifs du portefeuille métier"
    ]

# 🧩 Story complète
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
    exigences_typées = [(*typer_exigence(e), e) for e in exigences_brutes]
    critères = exigences_brutes[:3]
    tests = [
        f"Se connecter avec un compte {template['acteur']}",
        f"Accéder à la fonctionnalité : {template['action']}",
        f"Vérifier le résultat attendu lié à {template['objectif']}"
    ]
    validation = f"Le besoin métier « {template['objectif']} » est couvert par la fonctionnalité « {template['action']} »."
    suggestions = generer_suggestions_ia(template)
    return {
        "acteur": template["acteur"],
        "story": story,
        "exigences": exigences_typées,
        "critères": critères,
        "tests": tests,
        "validation": validation,
        "suggestions": suggestions
    }

# 🧠 Génération multi-acteurs
def generer_stories_depuis_besoin(requete):
    blocs = segmenter_requete(requete)
    all_stories = []
    for bloc in blocs:
        templates = reformuler_besoin(bloc)
        stories = [generer_story_complete(t) for t in templates]
        all_stories.extend(stories)
    return all_stories

# 📥 Markdown segmenté par acteur et type + BABOK
def formater_markdown(stories, _):
    md = "# 📘 Livrable segmenté par partie prenante\n"
    acteurs = {}
    for s in stories:
        acteurs.setdefault(s["acteur"], []).append(s)

    for acteur, bloc_stories in acteurs.items():
        md += f"\n# 🧑‍💼 {acteur.capitalize()}\n"
        exigences_par_type = {}
        for s in bloc_stories:
            for typ, babok, texte in s["exigences"]:
                exigences_par_type.setdefault(typ, []).append((texte, babok))
        md += "\n## 🟦 Exigences classées par type\n"
        for typ in ["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"]:
            if typ in exigences_par_type:
                md += f"\n### {typ}\n"
                for texte, babok in exigences_par_type[typ]:
                    md += f"- {texte} **({babok})**\n"
        md += f"\n## 📘 User Stories du {acteur}\n"
        for i, s in enumerate(bloc_stories, start=1):
            md += f"\n### 🧩 Story {i}\n"
            md += f"**User Story**\n{s['story']}\n\n"
            md += "**✅ Critères d’acceptation**\n"
            for c in s["critères"]:
                md += f"- {c}\n"
            md += "\n**🧪 Tests fonctionnels**\n"
            for t in s["tests"]:
                md += f"- {t}\n"
            md += f"\n**🔒 Validation métier**\n{s['validation']}\n"
            md += "\n**💡 Suggestions IA**\n"
            for sug in s["suggestions"]:
                md += f"- {sug}\n"

    md += "\n\n# 📘 Analyse selon le BABOK\n"
    md += "- **Besoin métier** : Problème ou opportunité exprimé par l’organisation\n"
    md += "- **Exigence métier** : Objectif stratégique ou opérationnel\n"
    md += "- **Exigence des parties prenantes** : Att
