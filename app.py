import streamlit as st
import joblib
import os

st.title("Classificador de sentimentos")

texto = st.text_input("Digite um tweet: ")

model_path = "./model.joblib"
vector_path = "./vectorizer.joblib"

if os.path.exists(model_path) and os.path.exists(vector_path):
   model = joblib.load(model_path)
   vectorizer = joblib.load(vector_path)
   
   if st.button("Analisar"):
      if texto.strip():
         vector = vectorizer.transform([texto])
         pred = model.predict(vector)[0]
         st.success(f"Sentimento: {pred}")
      else:
         st.warning("Por favor, insira um texto para análise.")
else:
   st.error("Modelo ou vetor não foram encontrados. Certifique que os arquivos model e vectozirer estão na raiz o projeto.")