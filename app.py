import streamlit as st
from pipeline import generer_stories_depuis_besoin
from io import BytesIO
from markdown import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="Pipeline IA Hybride", layout="wide")

st.title("🧠 Générateur de livrables métier par partie prenante")

with st.form("besoin_form"):
    requete = st.text_area("📝 Décris les besoins métier exprimés :", height=100)
    submitted = st.form_submit_button("🚀 Générer")

if submitted and requete:
    stories = generer_stories_depuis_besoin(requete)
    roles = sorted(set(s["acteur"] for s in stories))
    tabs = st.tabs([f"🧑‍💼 {r.capitalize()}" for r in roles] + ["📘 Exigences globales"])

    # Onglets par rôle (sans exigences BABOK)
    for i, role in enumerate(roles):
        with tabs[i]:
            st.subheader(f"📄 User Stories pour {role.capitalize()}")
            bloc = [s for s in stories if s["acteur"] == role]
            for idx, s in enumerate(bloc, start=1):
                st.markdown(f"### 🧩 Story {idx}")
                st.markdown(f"**User Story**\n\n{s['story']}")
                st.markdown("**✅ Critères d’acceptation**")
                for c in s["critères"]:
                    st.markdown(f"- {c}")
                st.markdown("**🧪 Tests fonctionnels**")
                for t in s["tests"]:
                    st.markdown(f"- {t}")
                st.markdown(f"**🔒 Validation métier**\n\n{s['validation']}")
                st.markdown("**💡 Suggestions IA**")
                for sug in s["suggestions"]:
                    st.markdown(f"- {sug}")

    # Onglet global avec sous-onglets par rôle pour les exigences BABOK
    with tabs[-1]:
        st.header("📘 Exigences BABOK par partie prenante")
        sous_tabs = st.tabs([f"🧑‍💼 {r.capitalize()}" for r in roles])
        for i, role in enumerate(roles):
            with sous_tabs[i]:
                bloc = [s for s in stories if s["acteur"] == role]
                for idx, s in enumerate(bloc, start=1):
                    st.markdown(f"### 🧩 Story {idx}")
                    st.markdown(f"**User Story**\n\n{s['story']}")
                    st.markdown("**📘 Exigences associées**")
                    for typ, babok, texte in s["exigences"]:
                        st.markdown(f"- **{typ}** : {texte}  \n↪ *({babok})*")

                # Export PDF individuel
                contenu_html = markdown("\n".join(s["babok"] for s in bloc))
                buffer = BytesIO()
                pisa.CreatePDF(contenu_html, dest=buffer)
                st.download_button(
                    label=f"📤 Télécharger les exigences de {role.capitalize()} en PDF",
                    data=buffer.getvalue(),
                    file_name=f"exigences_{role}.pdf",
                    mime="application/pdf"
                )
