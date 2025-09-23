import json
import os
from collections import defaultdict

RÉFÉRENTIEL_PATH = "data/referentiel_contextuel.json"

def charger_référentiel() -> dict:
    if not os.path.exists(RÉFÉRENTIEL_PATH):
        return defaultdict(list)
    with open(RÉFÉRENTIEL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_référentiel(référentiel: dict):
    with open(RÉFÉRENTIEL_PATH, "w", encoding="utf-8") as f:
        json.dump(référentiel, f, indent=2, ensure_ascii=False)

def enrichir_depuis_requête(requete: str):
    référentiel = charger_référentiel()
    lignes = [l.strip() for l in requete.split(".") if l.strip()]
    for ligne in lignes:
        for rôle in ["gestionnaire", "manager", "comptable", "client", "utilisateur"]:
            if rôle in ligne.lower():
                référentiel.setdefault(rôle, [])
                if ligne not in référentiel[rôle]:
                    référentiel[rôle].append(ligne)
    sauvegarder_référentiel(référentiel)

def extraire_connaissance(rôle: str) -> list:
    référentiel = charger_référentiel()
    return référentiel.get(rôle.lower(), [])
