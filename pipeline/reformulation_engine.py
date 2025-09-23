from pipeline.enrichissement_contextuel import extraire_connaissance

def reformuler_depuis_contexte(message: str, stories: list) -> str | None:
    msg = message.lower().strip()
    rôles_disponibles = sorted(set(s["acteur"].lower() for s in stories))

    for rôle in rôles_disponibles:
        if rôle in msg:
            connaissances = extraire_connaissance(rôle)
            if connaissances:
                exemples = "\n".join(f"- {c}" for c in connaissances[:3])
                return (
                    f"📚 Voici quelques attentes métier déjà exprimées pour le rôle **{rôle}** :\n"
                    f"{exemples}\n\nSouhaitez-vous que je vous affiche les exigences ou tests associés ?"
                )
    return None

