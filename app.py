import streamlit as st
from pipeline.orchestrateur_pipeline import orchestrer_pipeline
from pipeline.interaction_engine import repondre_intelligemment
import time

# Chargement du style iMessage
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Assistant IA — Analyse des besoins", layout="wide")
st.title("📊 Assistant IA — Analyse des besoins et génération de livrables")

# Initialisation des états
if "stories" not in st.session_state:
    st.session_state.stories = []
if "generated" not in st.session_state:
    st.session_state.generated = False
if "chat" not in st.session_state:
    st.session_state.chat = []

# Formulaire de génération
with st.form("besoin_form"):
    requete = st.text_area("📝 Décris les besoins métier exprimés :", height=100)
    privatiser = st.checkbox("🔐 Activer la privatisation des livrables")
    submitted = st.form_submit_button("🚀 Générer")

if submitted and requete:
    st.session_state.stories = orchestrer_pipeline(requete, privatiser=privatiser)
    st.session_state.generated = True
    st.session_state.chat = []

# Affichage des livrables si générés
if st.session_state.generated:
    stories = st.session_state.stories
    rôles = sorted(set(s["acteur"] for s in stories))
    tabs = st.tabs([f"🧑‍💼 {r.capitalize()}" for r in rôles] + ["📘 Exigences par rôle", "💬 Assistant IA"])

    # Onglets par rôle (1 story par rôle)
    for i, rôle in enumerate(rôles):
        with tabs[i]:
            s = next(story for story in stories if story["acteur"] == rôle)
            st.markdown(f"### 🧩 Story — {rôle.capitalize()}")
            st.markdown(f"**User Story**\n\n{s['story']}")
            st.markdown("**📘 Exigences BABOK**")
            for typ, babok, texte in s["exigences"]:
                st.markdown(f"- **{typ}** : {texte}  \n↪ *({babok})*")
            st.markdown("**✅ Critères d’acceptation**")
            for c in s["critères"]:
                st.markdown(f"- {c}")
            st.markdown("**🧪 Tests fonctionnels**")
            for t in s["tests"]:
                st.markdown(f"- {t}")
            st.markdown("**💡 Suggestions IA**")
            for sug in s["suggestions"]:
                st.markdown(f"- {sug}")
            st.markdown(f"**🔒 Validation métier**\n\n{s['validation']}")

    # Exigences par rôle
    with tabs[-2]:
        sous_tabs = st.tabs([f"🧑‍💼 {r.capitalize()}" for r in rôles])
        for i, rôle in enumerate(rôles):
            with sous_tabs[i]:
                s = next(story for story in stories if story["acteur"] == rôle)
                st.markdown(f"### 🧩 Story — {rôle.capitalize()}")
                st.markdown(f"**User Story**\n\n{s['story']}")
                st.markdown("**📘 Exigences associées**")
                for typ, babok, texte in s["exigences"]:
                    st.markdown(f"- **{typ}** : {texte}  \n↪ *({babok})*")

    # Assistant IA style iMessage
    with tabs[-1]:
        st.header("💬 Assistant IA — Style iMessage")

        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        for msg in st.session_state.chat:
            if msg["role"] == "user":
                st.markdown(f'''
                    <div class="user-wrapper">
                        <div class="user-bubble">{msg["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="assistant-wrapper">
                        <div class="assistant-bubble">{msg["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        user_input = st.chat_input("💬 Envoie un message comme dans iMessage…")
        if user_input:
            st.session_state.chat.append({"role": "user", "content": user_input})

            # Effet de frappe animé
            with st.empty():
                st.markdown('''
                    <div class="typing-indicator-wrapper">
                        <div class="typing-indicator">L’IA est en train d’écrire</div>
                    </div>
                ''', unsafe_allow_html=True)
                time.sleep(1.5)

            response = repondre_intelligemment(user_input, st.session_state.stories)
            st.session_state.chat.append({"role": "assistant", "content": response})
