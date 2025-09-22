import re

def repondre_chat(message: str, stories: list) -> str:
    message = message.lower().strip()
    mots_cles = re.findall(r"\w+", message)
    réponses = []

    rôles_disponibles = sorted(set(s["acteur"].lower() for s in stories))
    rôle_demandé = next((mot for mot in mots_cles if mot in rôles_disponibles), None)

    if not rôle_demandé:
        exemples = ", ".join(r.capitalize() for r in rôles_disponibles[:3])
        return (
            "🤖 Je n’ai pas trouvé ce rôle dans les livrables générés.\n"
            "Merci de vérifier que le rôle est bien mentionné dans la requête initiale.\n"
            f"Exemples de rôles disponibles : {exemples}…"
        )

    bloc = [s for s in stories if s["acteur"].lower() == rôle_demandé]
    for s in bloc:
        réponses.append(f"🧩 **{s['story']}**")
        réponses.append("✅ **Critères d’acceptation**")
        for c in s["critères"]:
            réponses.append(f"- {c}")
        réponses.append("🧪 **Tests principaux**")
        for t in s["tests"][:3]:
            réponses.append(f"- {t}")
        réponses.append("💡 **Suggestion IA**")
        réponses.append(f"- {s['suggestions'][0]}")
        réponses.append("🔒 **Validation**")
        réponses.append(s["validation"])
        réponses.append("")

    return "\n".join(réponses)
