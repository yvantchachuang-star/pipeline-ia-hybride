import streamlit as st
from pipeline import generer_stories_depuis_besoin
from io import BytesIO
from markdown import markdown
from xhtml2pdf import pisa

st.set_page_config(page_title="Pipeline IA Hybride", layout="wide")

st.title("🧠 Générateur de livrables métier par partie prenante")

requete = st.text_area("📝 Décris les besoins métier exprimés :", height=150)

if requete:
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

    # Onglet global pour exigences BABOK
    with tabs[-1]:
        st.header("📘 Exigences BABOK globales par partie prenante")

        type_selection = st.multiselect(
            "🔍 Filtrer par type d’exigence",
            options=["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"],
            default=["Métier", "Fonctionnelle", "Technique", "Partie prenante", "Non fonctionnelle"]
        )

        for role in roles:
            bloc = [s for s in stories if s["acteur"] == role]
            exigences_filtrées = []
            for s in bloc:
                for typ, babok, texte in s["exigences"]:
                    if typ in type_selection:
                        exigences_filtrées.append((typ, texte, babok))
            if exigences_filtrées:
                st.subheader(f"🧑‍💼 {role.capitalize()}")
                for typ in type_selection:
                    st.markdown(f"### {typ}")
                    for t, texte, babok in exigences_filtrées:
                        if t == typ:
                            st.markdown(f"- {texte} **({babok})**")

        # Export PDF global
        contenu_html = markdown("\n".join(s["babok"] for s in stories))
        buffer = BytesIO()
        pisa.CreatePDF(contenu_html, dest=buffer)
        st.download_button(
            label="📤 Télécharger toutes les exigences en PDF",
            data=buffer.getvalue(),
            file_name="exigences_globales.pdf",
            mime="application/pdf"
        )
