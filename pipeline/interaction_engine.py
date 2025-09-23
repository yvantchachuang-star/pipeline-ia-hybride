from pipeline.intention_engine import detecter_intention
from pipeline.assistant_engine import repondre_intelligemment

def repondre_chat(message: str, stories: list) -> str:
    # Optionnel : détecter l’intention pour enrichir plus tard
    intention = detecter_intention(message)
    return repondre_intelligemment(message, stories)
