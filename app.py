import streamlit as st
from pipeline import generer_stories_depuis_besoin, formater_markdown

st.set_page_config(page_title="Générateur de livrables", layout="wide")

st.title("📘 Générateur de livrables métier")
st.markdown("Formule ton besoin métier librement. Exemple : *Le gestionnaire de contrat d’assurance veut un système de gestion simple et sécurisé*")

besoin = st.text_area("✍️ Requête métier", height=100)

if "markdown" not in st.session_state:
    st.session_state.markdown = ""

if st.button("🚀 Générer livrables"):
    if besoin.strip():
        stories = generer_stories_depuis_besoin(besoin)
        exigences_globales = [ex for s in stories for ex in s["exigences"]]
        markdown = formater_markdown(stories, exigences_globales)
        st.session_state.markdown = markdown
        st.success("✅ Livrable généré avec succès.")
    else:
        st.warning("Merci de formuler un besoin métier avant de générer.")

if st.session_state.markdown:
    st.markdown("---")
    st.subheader("📄 Livrable généré")
    st.markdown(st.session_state.markdown)

    # 📥 Téléchargement du livrable
    st.download_button(
        label="📥 Télécharger le livrable (.md)",
        data=st.session_state.markdown,
        file_name="livrable_metier.md",
        mime="text/markdown"
    )
