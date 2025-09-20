import os
import shutil
import streamlit as st
from pipeline import generer_story_complete, generer_stories_depuis_besoin, formater_markdown

# 🔧 Corrige les erreurs de Watchdog sur Streamlit Cloud
os.environ["STREAMLIT_WATCHDOG_MODE"] = "poll"

# 🧹 Nettoyage automatique des fichiers parasites
if os.path.exists("__pycache__"):
    shutil.rmtree("__pycache__")
for f in os.listdir():
    if f.endswith(".pyc"):
        os.remove(f)

# 🧠 Configuration de l'app
st.set_page_config(page_title="Générateur de User Stories enrichies", layout="wide")
st.title("🧠 Générateur intelligent de User Stories")
st.write("✅ L'application est bien lancée")

# 📦 Initialisation de session
if "stories" not in st.session_state:
    st.session_state.stories = []

# 📝 Entrée utilisateur
besoin = st.text_input("Exprimez votre besoin métier (ex : le gestionnaire de contrat d'assurance souhaite un système de gestion simple et sécurisé)")

# 🚀 Génération initiale
if st.button("Générer"):
    st.session_state.stories = generer_stories_depuis_besoin(besoin)

# 🧩 Affichage des stories
if st.session_state.stories:
    exigences_globales = []
    for s in st.session_state.stories:
        exigences_globales.extend(s["exigences"])

    # 📘 Exigences classées
    st.markdown("## 📘 Exigences classées par type")
    types = ["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"]
    for t in types:
        st.markdown(f"### 🟦 {t}")
        for typ, texte in exigences_globales:
            if typ == t:
                st.markdown(f"- {texte}")
    st.markdown("---")

    # 🧩 Stories enrichies
    for i, s in enumerate(st.session_state.stories, start=1):
        st.markdown(f"## 🧩 Story {i}")
        st.markdown(f"**User Story**\n{s['story']}")
        st.markdown("**✅ Critères d’acceptation**")
        for c in s["critères"]:
            st.markdown(f"- {c}")
        st.markdown("**🧪 Tests fonctionnels**")
        for t in s["tests"]:
            st.markdown(f"- {t}")
        st.markdown(f"**🔒 Validation métier**\n{s['validation']}")
        st.markdown("**💡 Suggestions IA**")
        for suggestion in s["suggestions"]:
            if st.button(suggestion, key=f"{i}-{suggestion}"):
                st.success(f"✅ Suggestion sélectionnée : {suggestion}")

    # 📥 Export Markdown
    markdown_result = formater_markdown(st.session_state.stories, exigences_globales)
    st.download_button("📥 Télécharger le Markdown", markdown_result, file_name="user_stories.md")

    # ➕ Ajout dynamique
    with st.expander("➕ Ajouter une partie prenante ou un besoin complémentaire"):
        nouveau_role = st.text_input("Nom de la partie prenante (ex : auditeur, client)", key="role")
        nouvelle_action = st.text_input("Action souhaitée (ex : consulter les contrats)", key="action")
        nouvel_objectif = st.text_input("Objectif métier (ex : suivre mes engagements)", key="objectif")
        if st.button("Ajouter cette story", key="ajouter_story"):
            nouvelle_story = {
                "acteur": nouveau_role,
                "action": nouvelle_action,
                "objectif": nouvel_objectif
            }
            st.session_state.stories.append(generer_story_complete(nouvelle_story))
            st.success(f"Story ajoutée pour {nouveau_role}")
