import streamlit as st
from pipeline import generer_stories_depuis_besoin, formater_markdown
from io import BytesIO
from markdown import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="Générateur de livrables", layout="wide")

st.title("📘 Générateur de livrables métier")
st.markdown("Formule ton besoin métier librement. Exemple : *Le gestionnaire de contrat d’assurance veut un système de gestion simple et sécurisé*")

# Champ de saisie
besoin = st.text_area("✍️ Requête métier", height=100)

# Initialisation
if "markdown" not in st.session_state:
    st.session_state.markdown = ""
if "stories" not in st.session_state:
    st.session_state.stories = []

# Bouton de génération
if st.button("🚀 Générer livrables"):
    if besoin.strip():
        stories = generer_stories_depuis_besoin(besoin)
        exigences_globales = [ex for s in stories for ex in s["exigences"]]
        markdown_text = formater_markdown(stories, exigences_globales)
        st.session_state.markdown = markdown_text
        st.session_state.stories = stories
        st.success("✅ Livrable généré avec succès.")
    else:
        st.warning("Merci de formuler un besoin métier avant de générer.")

# Affichage par rôle
if st.session_state.stories:
    st.markdown("---")
    st.subheader("📄 Livrable par rôle métier")

    # Regrouper par acteur
    acteurs = {}
    for s in st.session_state.stories:
        acteur = s["acteur"]
        if acteur not in acteurs:
            acteurs[acteur] = []
        acteurs[acteur].append(s)

    tabs = st.tabs([a.capitalize() for a in acteurs.keys()])
    for tab, acteur in zip(tabs, acteurs.keys()):
        with tab:
            for i, s in enumerate(acteurs[acteur], start=1):
                st.markdown(f"### 🧩 Story {i}")
                st.markdown(f"**User Story**\n\n{s['story']}")
                st.markdown("**✅ Critères d’acceptation**")
                for c in s["critères"]:
                    st.markdown(f"- {c}")
                st.markdown("**🧪 Tests fonctionnels**")
                for t in s["tests"]:
                    st.markdown(f"- {t}")
                st.markdown("**🔒 Validation métier**")
                st.markdown(s["validation"])
                st.markdown("**💡 Suggestions IA**")
                for sug in s["suggestions"]:
                    st.markdown(f"- {sug}")

# 📦 Export du livrable
if st.session_state.markdown:
    st.markdown("---")
    st.subheader("📦 Export du livrable")

    # Téléchargement Markdown
    st.download_button(
        label="📥 Télécharger le livrable (.md)",
        data=st.session_state.markdown,
        file_name="livrable_metier.md",
        mime="text/markdown"
    )

    # Conversion Markdown → PDF
    def convertir_markdown_en_pdf(markdown_text):
        html = markdown(markdown_text)
        pdf_buffer = BytesIO()
        pisa.CreatePDF(html, dest=pdf_buffer)
        return pdf_buffer.getvalue()

    pdf_bytes = convertir_markdown_en_pdf(st.session_state.markdown)
    st.download_button(
        label="📄 Télécharger le livrable (.pdf)",
        data=pdf_bytes,
        file_name="livrable_metier.pdf",
        mime="application/pdf"
    )
