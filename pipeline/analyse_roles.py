import re

def analyse_roles(requete: str) -> list:
    candidats = re.findall(r"\ble (\w+)", requete.lower()) + \
                re.findall(r"\bla (\w+)", requete.lower()) + \
                re.findall(r"\ben tant que (\w+)", requete.lower())
    return list(set(candidats)) or ["utilisateur"]
