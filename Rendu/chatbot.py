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


def show_ui():
    
    st.title("Chatbot")    
    st.image("Robot2.png", width=500)
    #st.subheader("Entrer votre question :) ")
    #Initialise le chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.chat_history = []

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accepte la question de l'utilisateur
    if prompt := st.chat_input("Enter votre question :) "):
        with st.spinner("Patience ...."):     
            response = query(question=prompt, chat_history=st.session_state.chat_history)            
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("Assistant"):
                st.markdown(response["answer"])    

            # Append user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "Assistant", "content": response["answer"]})
            st.session_state.chat_history.extend([(prompt, response["answer"])])


if __name__ == "__main__":
    show_ui() 
