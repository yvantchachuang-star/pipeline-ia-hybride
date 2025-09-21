from .analyse_roles import analyse_roles
from .gen_objectifs import gen_objectifs
from .gen_story import gen_story

def generer_stories_depuis_besoin(requete: str) -> list:
    rôles = analyse_roles(requete)
    stories = []
    for rôle in rôles:
        objectifs = gen_objectifs(rôle)
        for obj in objectifs:
            stories.append(gen_story(rôle, obj))
    return stories

