import streamlit as st
from pipeline import traiter_user_story

st.set_page_config(page_title="Pipeline IA Hybride", layout="wide")

st.title("🧠 Pipeline IA Hybride")
st.markdown("Entrez une user story pour générer automatiquement les spécifications, tests et validation métier.")

user_story = st.text_area("User Story", height=150)

if st.button("Lancer le pipeline"):
    if user_story.strip():
        synthese = traiter_user_story(user_story)
        st.markdown(synthese)
    else:
        st.warning("Veuillez entrer une user story.")
