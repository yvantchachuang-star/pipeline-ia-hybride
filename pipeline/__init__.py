from .analyse_roles import analyse_roles
from .gen_objectifs import gen_objectifs
from .gen_story import gen_story
from .gen_exigences import gen_exigences

def generer_stories_depuis_besoin(requete: str) -> list:
    rôles = analyse_roles(requete)
    stories = []
    for rôle in rôles:
        objectifs = gen_objectifs(rôle)
        for obj in objectifs:
            bloc = gen_story(rôle, obj)
            bloc["exigences"] = gen_exigences(rôle, obj)
            bloc["babok"] = f"Exigence métier identifiée pour le rôle {rôle}, liée à l'objectif : {obj}."
            stories.append(bloc)
    return stories
