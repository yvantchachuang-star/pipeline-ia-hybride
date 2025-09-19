import streamlit as st
from pipeline import generer_stories_depuis_besoin, formater_markdown

st.set_page_config(page_title="Générateur de User Stories enrichies", layout="wide")
st.title("🧠 Générateur intelligent de User Stories")

besoin = st.text_input("Exprimez votre besoin métier")

if st.button("Générer"):
    stories = generer_stories_depuis_besoin(besoin)

    exigences_globales = []
    for s in stories:
        exigences_globales.extend(s["exigences"])

    st.markdown("## 📘 Exigences classées par type")
    types = ["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"]
    for t in types:
        st.markdown(f"### 🟦 {t}")
        for typ, texte in exigences_globales:
            if typ == t:
                st.markdown(f"- {texte}")

    for i, s in enumerate(stories, start=1):
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

    st.markdown("---")
    st.markdown("## 📘 Définition des types d’exigences")
    st.markdown("""
- **Métier** : Objectifs ou besoins exprimés par l’organisation (valeur, efficacité, conformité)  
- **Fonctionnelle** : Comportement attendu du système (actions, interfaces, règles)  
- **Technique** : Contraintes d’architecture, performance, sécurité, formats  
- **Partie prenante** : Besoins spécifiques d’un acteur (client, gestionnaire, partenaire)  
- **Non fonctionnelle** : Qualités du système (temps de réponse, accessibilité, robustesse, ergonomie)
    """)

    markdown_result = formater_markdown(stories, exigences_globales)
    st.download_button("📥 Télécharger le Markdown", markdown_result, file_name="user_stories.md")



