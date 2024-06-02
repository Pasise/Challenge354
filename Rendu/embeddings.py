import json
from pathlib import Path
from pprint import pprint
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings 
from langchain_community.vectorstores import FAISS

def upload_data():
    file_path = "extracted_data.json"

    loader = JSONLoader(
        file_path=file_path,
        jq_schema=".data[]",  # Utilisation de ".data[]" pour sélectionner chaque élément dans la liste "data"
        content_key=".article",  # Utilisation de ".article" pour sélectionner chaque objet "article" dans chaque élément de la liste "data"
        is_content_key_jq_parsable=True,
        text_content=False  # Indique que le contenu n'est pas une chaîne de caractères
    )

    data = loader.load()

    # Split les documents en chunks de texte
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]        
    )

    split_documents = text_splitter.split_documents(documents=data)
    print(f"Split into {len(split_documents)} Documents...")

    # Sauvegarde des documents
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(split_documents, embeddings)
    # Sauvegarde de la base de données
    db.save_local("faiss_index2")

def faiss_query():
    
    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index2", embeddings, allow_dangerous_deserialization=True)

    query = "Explain the Candidate Onboarding process."
    docs = new_db.similarity_search(query)

    # Afficher le contenu des documents
    for doc in docs:
        print("##---- Page ---##")
        print(doc.metadata['source'])
        print("##---- Content ---##")
        print(doc.page_content)

if __name__ == "__main__":
    #Le code ci-dessous "upload_htmls()" est exécuté une seule fois, puis commenté, car la base de données 
    #vectorielle est prête 
    upload_data()   
    
    faiss_query()
