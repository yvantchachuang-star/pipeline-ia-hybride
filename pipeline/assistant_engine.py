import re

def proposer_analyses(stories, rôle):
    analyses = []
    objectifs = [s["story"] for s in stories if s["acteur"].lower() == rôle]
    exigences = [e for s in stories if s["acteur"].lower() == rôle for e in s["exigences"]]
    tests = [t for s in stories if s["acteur"].lower() == rôle for t in s["tests"]]

    types = [e[0] for e in exigences]
    if len(objectifs) < 2:
        analyses.append(f"🔍 Le rôle **{rôle}** semble sous-représenté : seulement {len(objectifs)} user story générée.")
    else:
        analyses.append(f"📊 Le rôle **{rôle}** couvre {len(objectifs)} objectifs métier. Cela permet une bonne traçabilité.")
    if "Réglementaire" not in types:
        analyses.append("⚠️ Aucune exigence réglementaire détectée. Vérifier les obligations légales ou sectorielles.")
    if "Qualité" in types:
        analyses.append("✅ Des exigences de qualité sont présentes, ce qui renforce la robustesse fonctionnelle.")
    if any("temps de réponse" in t.lower() for t in tests):
        analyses.append("⏱ Des tests de performance sont prévus. Pensez à définir des seuils mesurables.")
    return analyses


def repondre_chat(message: str, stories: list) -> str:
    message = message.lower().strip()
    mots_cles = re.findall(r"\w+", message)
    réponses = []

    # Réponses relationnelles ou polies
    if message in ["bonjour", "salut", "hello", "bonsoir"]:
        return "Bonjour. Je suis disponible pour vous aider à explorer les livrables métier ou les exigences BABOK."
    if message in ["comment tu vas", "ça va", "tu es là", "tu vas bien", "tu es fatigué", "tu dors"]:
        return "Je suis opérationnel et prêt à vous assister. Souhaitez-vous explorer un rôle métier ou une exigence particulière ?"
    if message in ["merci", "merci beaucoup", "je te remercie"]:
        return "Avec plaisir. N'hésitez pas à poser une autre question métier ou technique."
    if message in ["au revoir", "bye", "à bientôt"]:
        return "Au revoir. Je reste disponible pour toute analyse métier ou question technique."

    # Détection du rôle demandé
    rôles_disponibles = sorted(set(s["acteur"].lower() for s in stories))
    rôle_demandé = next((mot for mot in mots_cles if mot in rôles_disponibles), None)

    if not rôle_demandé:
        exemples = ", ".join(r.capitalize() for r in rôles_disponibles[:3])
        return (
            "🤖 Je n’ai pas trouvé ce rôle dans les livrables générés.\n"
            "Merci de vérifier que le rôle est bien mentionné dans la requête initiale.\n"
            f"Exemples de rôles disponibles : {exemples}…"
        )

    # Filtrage des livrables
    bloc = [s for s in stories if s["acteur"].lower() == rôle_demandé]
    for s in bloc:
        résumé = f"🧩 **{s['story']}**"
        exigences = [f"- {typ} : {texte}" for typ, _, texte in s["exigences"]]
        critères = ", ".join(s["critères"])
        tests = s["tests"][:2]
        suggestions = s["suggestions"][:1]

        réponses.append(résumé)
        réponses.append("📘 **Exigences clés**")
        réponses.extend(exigences[:3])
        réponses.append(f"✅ **Critères** : {critères}")
        réponses.append("🧪 **Tests principaux**")
        for t in tests:
            réponses.append(f"- {t}")
        réponses.append("💡 **Suggestion IA**")
        réponses.append(f"- {suggestions[0]}")
        réponses.append("🔒 **Validation**")
        réponses.append(s["validation"])
        réponses.append("")

    # Pistes d’analyse
    analyses = proposer_analyses(stories, rôle_demandé)
    if analyses:
        réponses.append("📌 **Pistes d’analyse métier**")
        réponses.extend(analyses)

    return "\n".join(réponses)

