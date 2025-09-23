import json
import os
from collections import defaultdict

# 📁 Chemin du fichier de référentiel
RÉFÉRENTIEL_PATH = "data/referentiel_contextuel.json"

# 📥 Chargement du référentiel existant
def charger_référentiel() -> dict:
    if not os.path.exists(RÉFÉRENTIEL_PATH):
        return defaultdict(list)
    with open(RÉFÉRENTIEL_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# 💾 Sauvegarde du référentiel enrichi
def sauvegarder_référentiel(référentiel: dict):
    dossier = os.path.dirname(RÉFÉRENTIEL_PATH)
    if not os.path.exists(dossier):
        os.makedirs(dossier)  # ✅ Crée le dossier s’il n’existe pas
    with open(RÉFÉRENTIEL_PATH, "w", encoding="utf-8") as f:
        json.dump(référentiel, f, indent=2, ensure_ascii=False)

# 🔁 Enrichissement automatique depuis une requête métier
def enrichir_depuis_requête(requete: str):
    référentiel = charger_référentiel()
    lignes = [l.strip() for l in requete.split(".") if l.strip()]
    rôles_candidats = ["gestionnaire", "manager", "comptable", "client", "utilisateur", "administrateur", "opérateur"]

    for ligne in lignes:
        for rôle in rôles_candidats:
            if rôle in ligne.lower():
                référentiel.setdefault(rôle, [])
                if ligne not in référentiel[rôle]:
                    référentiel[rôle].append(ligne)
    sauvegarder_référentiel(référentiel)

# 🔍 Extraction des connaissances métier pour un rôle donné
def extraire_connaissance(rôle: str) -> list:
    référentiel = charger_référentiel()
    return référentiel.get(rôle.lower(), [])
