def repondre_chat(message: str, stories: list) -> str:
    message = message.lower()
    réponses = []

    for s in stories:
        if message in s["acteur"] or message in s["story"].lower():
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

