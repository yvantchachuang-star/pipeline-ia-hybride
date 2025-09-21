from .analyse_roles import analyse_roles
from .gen_objectifs import gen_objectifs
from .gen_story import gen_story
from .gen_exigences import gen_exigences
from .gen_tests import gen_tests

def generer_stories_depuis_besoin(requete: str) -> list:
    """
    Orchestration complète : à partir d'une requête métier,
    génère les user stories, exigences BABOK et scénarios de test.
    """
    rôles = analyse_roles(requete)
    stories = []

    for rôle in rôles:
        objectifs = gen_objectifs(rôle)
        for obj in objectifs:
            bloc = gen_story(rôle, obj)
            bloc["exigences"] = gen_exigences(rôle, obj)
            bloc["tests"] = gen_tests(rôle, obj)
            bloc["babok"] = f"Exigences BABOK générées pour le rôle {rôle}, objectif : {obj}."
            stories.append(bloc)

    return stories
