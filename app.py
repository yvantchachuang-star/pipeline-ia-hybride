import streamlit as st
from pipeline import traiter_user_story

st.set_page_config(page_title="Pipeline IA Hybride", layout="wide")

st.title("🧠 Pipeline IA Hybride")
st.markdown("Entrez une user story pour générer automatiquement les spécifications, tests et validation métier.")

user_stories = st.text_area("User Stories (une par ligne)", height=250)

if st.button("Lancer le pipeline"):
    lignes = [l.strip() for l in user_stories.split("\n") if l.strip()]
    for i, story in enumerate(lignes, start=1):
        st.markdown(f"## 🧩 Story {i}")
        synthese = traiter_user_story(story)
        st.markdown(synthese)

