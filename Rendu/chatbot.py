from langchain_openai import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

def query(question, chat_history):
    
    #Telechargement de la base de données vectorielle
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index2", embeddings, allow_dangerous_deserialization=True)  
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    # Création de la chaîne de récupération conversationnelle
    query = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=new_db.as_retriever(), 
        return_source_documents=True)
    # Requête de la chaîne de récupération
    return query({"question": question, "chat_history": chat_history})

def format_prompt(prompt):
    instructions = """
    Tu es un assistant intelligent qui peut répondre en plus à des questions en relation avec le site Ecofin 
    Ecofin est une plateforme en ligne de premier plan qui fournit une couverture complète des actualités 
    économiques, financières et commerciales, avec un accent particulier sur l'Afrique.
    L'agence couvre divers secteurs, notamment la finance, l'énergie, les télécommunications, la gestion publique
    et les infrastructures, visant à offrir des informations pertinentes et à jour sur les marchés et 
    les économies africaines​. 
    Exemple de question : 
    - "Que s'est il passé au Togo récemment?" 
      Réponse attendue : "Le Togo bénéficiera d’un financement japonais de 1,2 milliard FCFA pour appuyer son secteur agricole"

    Question : """ + prompt
    return instructions


def show_ui():
    st.title("Chatbot")    
    st.image("Robot2.png", width=500)
    
    # Initialiser l'historique du chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accepter la question de l'utilisateur
    if prompt := st.chat_input("Entrez votre question :) "):
        formatted_prompt = format_prompt(prompt)
        with st.spinner("Patience ...."):     
            response = query(question=formatted_prompt, chat_history=st.session_state.chat_history)
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("Assistant"):
                st.markdown(response["answer"])    

            # Ajouter le message de l'utilisateur à l'historique du chat
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "Assistant", "content": response["answer"]})
            st.session_state.chat_history.extend([(prompt, response["answer"])])

if __name__ == "__main__":
    show_ui()