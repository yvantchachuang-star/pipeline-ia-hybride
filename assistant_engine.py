import re

def repondre_chat(message: str, stories: list) -> str:
    message = message.lower()
    mots_cles = re.findall(r"\w+", message)
    réponses = []

    for s in stories:
        rôle = s["acteur"].lower()
        story = s["story"].lower()

        # Détection par rôle
        match_rôle = rôle in message or any(rôle in mot for mot in mots_cles)

        # Détection par mots-clés dans story
        match_story = any(mot in story for mot in mots_cles)

        # Détection dans exigences
        match_exigences = any(
            any(mot in texte.lower() or mot in babok.lower() or mot in typ.lower()
                for mot in mots_cles)
            for typ, babok, texte in s.get("exigences", [])
        )

        # Détection dans critères
        match_critères = any(any(mot in c.lower() for mot in mots_cles) for c in s["critères"])

        # Détection dans tests
        match_tests = any(any(mot in t.lower() for mot in mots_cles) for t in s["tests"])

        # Détection dans suggestions
        match_suggestions = any(any(mot in sug.lower() for mot in mots_cles) for sug in s["suggestions"])

        # Détection dans validation
        match_validation = any(mot in s["validation"].lower() for mot in mots_cles)

        if match_rôle or match_story or match_exigences or match_critères or match_tests or match_suggestions or match_validation:
            réponses.append(f"### 🧩 User Story ({s['acteur'].capitalize()})\n{s['story']}")

            if s.get("exigences"):
                réponses.append("📘 **Exigences BABOK**")
                for typ, babok, texte in s["exigences"]:
                    réponses.append(f"- **{typ}** : {texte}  \n↪ *({babok})*")

            réponses.append("✅ **Critères d’acceptation**")
            for c in s["critères"]:
                réponses.append(f"- {c}")

            réponses.append("🧪 **Tests fonctionnels**")
            for t in s["tests"]:
                réponses.append(f"- {t}")

            réponses.append("💡 **Suggestions IA**")
            for sug in s["suggestions"]:
                réponses.append(f"- {sug}")

            réponses.append("🔒 **Validation métier**")
            réponses.append(f"{s['validation']}")
            réponses.append("")

    if réponses:
        return "\n".join(réponses)
    else:
        return (
            "🤖 Je n’ai pas trouvé de livrable correspondant à ta demande.\n"
            "Essaie avec un rôle métier, un mot-clé métier, ou un type d’exigence (ex : fonctionnelle, métier, test…)."
        )
