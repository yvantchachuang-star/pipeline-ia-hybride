import streamlit as st
from pipeline import generer_stories_depuis_besoin
from assistant_engine import repondre_chat

st.set_page_config(page_title="Assistant IA — Analyse des besoins", layout="wide")
st.title("📊 Assistant IA — Analyse des besoins et génération de livrables")

with st.form("besoin_form"):
    requete = st.text_area("📝 Décris les besoins métier exprimés :", height=100)
    submitted = st.form_submit_button("🚀 Générer")

if submitted and requete:
    stories = generer_stories_depuis_besoin(requete)
    roles = sorted(set(s["acteur"] for s in stories))
    tabs = st.tabs([f"🧑‍💼 {r.capitalize()}" for r in roles] + ["📘 Exigences par rôle", "💬 Assistant IA"])

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

    with tabs[-2]:
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

    with tabs[-1]:
        st.header("💬 Assistant IA — Dialogue métier")
        if "chat" not in st.session_state:
            st.session_state.chat = []

        for msg in st.session_state.chat:
            st.chat_message(msg["role"]).markdown(msg["content"])

        user_input = st.chat_input("Pose une question métier ou technique…")
        if user_input:
            st.session_state.chat.append({"role": "user", "content": user_input})
            response = repondre_chat(user_input, stories)
            st.session_state.chat.append({"role": "assistant", "content": response})
            st.chat_message("assistant").markdown(response)
