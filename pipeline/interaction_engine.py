from pipeline.intention_engine import detecter_intention
from pipeline.reformulation_engine import reformuler_question
from pipeline.assistant_engine import repondre_chat

def repondre_intelligemment(message: str, stories: list) -> str:
    """
    Gère les échanges conversationnels : politesse, relationnel, métier, reformulation.
    Bascule vers le moteur métier si besoin.
    """
    intention = detecter_intention(message)

    if intention == "salutation":
        return "Bonjour. Je suis prêt à vous aider à explorer les livrables métier ou les exigences BABOK."

    if intention == "relationnel":
        return "Je suis opérationnel et disponible. Souhaitez-vous explorer un rôle métier ou une exigence particulière ?"

    if intention == "politesse":
        return "Avec plaisir. Je reste à votre disposition pour toute autre analyse métier."

    if intention == "métier":
        return repondre_chat(message, stories)

    # Si intention inconnue, tenter une reformulation
    reformulation = reformuler_question(message)
    if reformulation:
        return f"🤖 Je reformule votre demande :\n{reformulation}"

    return "Je n’ai pas compris votre intention. Pouvez-vous préciser votre demande métier ou technique ?"
