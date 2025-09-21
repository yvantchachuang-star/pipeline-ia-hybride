def detecter_intention(message: str) -> str:
    msg = message.lower().strip()

    if msg in ["bonjour", "salut", "hello", "bonsoir"]:
        return "salutation"
    if "comment tu vas" in msg or "ça va" in msg or "tu es là" in msg or "tu vas bien" in msg:
        return "relationnel"
    if "merci" in msg or "au revoir" in msg or "bye" in msg or "à bientôt" in msg:
        return "politesse"
    if "exigence" in msg or "test" in msg or "story" in msg or "critère" in msg or "livrable" in msg:
        return "métier"
    return "inconnu"
