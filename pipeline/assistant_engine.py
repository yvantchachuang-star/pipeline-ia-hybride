from pipeline.reformulation_engine import reformuler_depuis_contexte

def repondre_intelligemment(message: str, stories: list) -> str:
    msg = message.lower().strip()
    rôles_disponibles = sorted(set(s["acteur"].lower() for s in stories))

    # 🔁 Reformulation contextuelle
    reformulation = reformuler_depuis_contexte(msg, stories)
    if reformulation:
        return reformulation

    # 🔍 Détection du rôle
    rôle_demandé = next((r for r in rôles_disponibles if r in msg), None)
    if not rôle_demandé:
        exemples = ", ".join(r.capitalize() for r in rôles_disponibles[:3])
        return f"🤖 Je n’ai pas trouvé ce rôle dans les livrables générés.\nExemples : {exemples}…"

    bloc = [s for s in stories if s["acteur"].lower() == rôle_demandé]
    if not bloc:
        return f"🤖 Aucun livrable trouvé pour le rôle {rôle_demandé}."

    s = bloc[0]
    réponse = []

    if "exigence" in msg:
        réponse.append("📘 **Exigences BABOK**")
        for typ, babok, texte in s["exigences"]:
            réponse.append(f"- **{typ}** : {texte}  \n↪ *({babok})*")
    elif "test" in msg:
        réponse.append("🧪 **Tests fonctionnels**")
        for t in s["tests"]:
            réponse.append(f"- {t}")
    elif "suggestion" in msg:
        réponse.append("💡 **Suggestions IA**")
        for sug in s["suggestions"]:
            réponse.append(f"- {sug}")
    else:
        réponse.append(f"🧩 **User Story**\n{s['story']}")
        réponse.append("✅ **Critères d’acceptation**")
        for c in s["critères"]:
            réponse.append(f"- {c}")
        réponse.append("🧪 **Tests principaux**")
        for t in s["tests"][:3]:
            réponse.append(f"- {t}")
        réponse.append("💡 **Suggestion IA**")
        réponse.append(f"- {s['suggestions'][0]}")
        réponse.append("🔒 **Validation**")
        réponse.append(s["validation"])

    return "\n".join(réponse)
