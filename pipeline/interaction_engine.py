from pipeline.intention_engine import detecter_intention
from pipeline.reformulation_engine import reformuler_question
from pipeline.assistant_engine import repondre_chat

def repondre_intelligemment(message: str, stories: list) -> str:
    intention = detecter_intention(message)

    if intention == "salutation":
        return "👋 Hello ! Je suis prêt à t’aider à explorer les livrables métier ou les exigences BABOK."

    if intention == "relationnel":
        return "😄 Toujours là ! Tu veux qu’on parle d’un rôle métier ou d’un test fonctionnel ?"

    if intention == "politesse":
        return "🙏 Avec plaisir. Je reste à ta disposition pour toute autre analyse métier."

    if intention == "métier":
        return repondre_chat(message, stories)

    reformulation = reformuler_question(message)
    if reformulation:
        return f"🤖 Hmm… tu veux dire :\n👉 {reformulation}"

    return "🤔 Je n’ai pas compris ta demande. Tu peux préciser un rôle métier, une exigence ou un test ?"
