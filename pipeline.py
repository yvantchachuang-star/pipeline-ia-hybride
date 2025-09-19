import re

def traiter_user_story(user_story):
    # Extraction NLP
    def extraire_elements(user_story):
        user_story = user_story.lower()
        acteur = re.findall(r"en tant que (\w+)", user_story)
        action = re.findall(r"je veux (\w+.*?) (?:afin|pour|dans|depuis|avec|et|\.|$)", user_story)
        objectif = re.findall(r"(?:afin de|pour) (.+)", user_story)
        contexte = re.findall(r"(?:depuis|dans|avec) (mon .*?|l’.*?|un .*?)", user_story)
        return {
            "acteur": acteur[0] if acteur else "inconnu",
            "action": action[0] if action else "inconnu",
            "objectif": objectif[0] if objectif else "non précisé",
            "contexte": contexte[0] if contexte else "non précisé"
        }

    # Spécifications
    def generer_specifications(elements):
        user_story = f"En tant que {elements['acteur']}, je veux {elements['action']} afin de {elements['objectif']}."
        criteres = [
            f"L’utilisateur peut {elements['action']}",
            f"Les données sont accessibles depuis {elements.get('contexte', 'l’interface')}",
            "En cas d’erreur, un message clair est affiché"
        ]
        description = f"""
        Fonctionnalité : {elements['action'].capitalize()}
        Acteur : {elements['acteur'].capitalize()}
        Objectif : {elements['objectif']}
        Contexte : {elements.get('contexte', 'non précisé')}
        """
        return {
            "user_story": user_story,
            "criteres_acceptation": criteres,
            "description_fonctionnelle": description.strip()
        }

    # Tests
    def generer_tests(specs):
        criteres = specs.get("criteres_acceptation", [])
        tests = []
        for i, critere in enumerate(criteres, start=1):
            test = {
                "titre": f"Test {i} : {critere}",
                "preconditions": "L’utilisateur est connecté à son espace personnel.",
                "etapes": [
                    "Accéder à l’espace personnel",
                    f"Effectuer l’action : {critere}"
                ],
                "resultat_attendu": f"{critere} est satisfait sans erreur"
            }
            tests.append(test)
        return tests

    # Validation métier
    def valider_specifications(specs, tests):
        erreurs = []
        criteres = specs.get("criteres_acceptation", [])
        titres_tests = [t["titre"].lower() for t in tests]

        for critere in criteres:
            if critere.lower() not in " ".join(titres_tests):
                erreurs.append(f"Critère non couvert par les tests : {critere}")

        if "description_fonctionnelle" in specs and "user_story" in specs:
            if specs["description_fonctionnelle"].lower() not in specs["user_story"].lower():
                erreurs.append("Incohérence entre user story et description fonctionnelle")

        if "facture" in specs.get("user_story", "").lower() and "client" not in specs.get("user_story", "").lower():
            erreurs.append("Accès aux factures réservé aux clients — rôle incohérent")

        return erreurs if erreurs else ["✅ Spécifications validées"]

    # Synthèse
    def generer_synthese(specs, tests, validation):
        synthese = f"# 📄 Synthèse fonctionnelle\n\n"
        synthese += f"## 🧠 User Story\n{specs.get('user_story', 'Non disponible')}\n\n"
        synthese += f"## ✅ Critères d’acceptation\n"
        for c in specs.get("criteres_acceptation", []):
            synthese += f"- {c}\n"
        synthese += f"\n## 🔍 Description fonctionnelle\n{specs.get('description_fonctionnelle', 'Non disponible')}\n\n"
        synthese += f"## 🧪 Tests fonctionnels\n"
        for t in tests:
            synthese += f"### {t['titre']}\n"
            synthese += f"- Préconditions : {t['preconditions']}\n"
            synthese += f"- Étapes :\n"
            for e in t['etapes']:
                synthese += f"  - {e}\n"
            synthese += f"- Résultat attendu : {t['resultat_attendu']}\n\n"
        synthese += f"## 🔒 Validation métier\n"
        for v in validation:
            synthese += f"- {v}\n"
        return synthese

    # Pipeline complet
    elements = extraire_elements(user_story)
    specs = generer_specifications(elements)
    tests = generer_tests(specs)
    validation = valider_specifications(specs, tests)
    synthese = generer_synthese(specs, tests, validation)
    return synthese

def extraire_elements(user_story):
    user_story = user_story.lower()
    acteur = re.findall(r"en tant que (\w+)", user_story)
    action = re.findall(r"(?:je veux|je souhaite|je peux|je dois) (.+?) (?:afin|pour|dans|depuis|avec|et|\.|$)", user_story)
    objectif = re.findall(r"(?:afin de|pour) (.+)", user_story)
    contexte = re.findall(r"(?:depuis|dans|avec) (mon .*?|l’.*?|un .*?)", user_story)
    return {
        "acteur": acteur[0] if acteur else "inconnu",
        "action": action[0] if action else "inconnu",
        "objectif": objectif[0] if objectif else "non précisé",
        "contexte": contexte[0] if contexte else "non précisé"
    }

