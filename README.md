# Challenge

L'objectif de ce challenge est de récupérer les articles sur le site [Agence Ecofin](https://www.agenceecofin.com/a-la-une/recherche-article?filterTitle=&submit.x=0&submit.y=0&filterTousLesFils=Tous&filterCategories=Sous-rubrique&filterDateFrom=&filterDateTo=&option=com_dmk2articlesfilter&view=articles&filterFrench=French&Itemid=269&userSearch=1&layout=#dmk2articlesfilter_results), les traiter et les stocker. Ensuite de créer une chaîne de traitement pour le RAG (Retrieve, Analyse, Generate) des articles pouvant s'utiliser grâce à une interface pour interagir avec.

## Installation de l'environnement

Pour ce projet j'ai utilisé un environnement virtuel Python. Pour l'installer vous pouvez suivre les instructions suivantes:

1. Créez un dossier :
    ```bash
    mkdir Votre_dossier
    cd Votre_dossier
    ```

2. Procédez à l'installation de l'environnement virtuel :
    ```bash
    pipenv shell
    ```

    Si vous n'avez pas pipenv, vous pouvez l'installer en utilisant l'une des commandes suivantes :
    ```bash
    pip install --user pipenv
    ```
    ou
    ```bash
    brew install pipenv
    ```

3. Installez les packages nécessaires :
    ```bash
    pipenv install langhchain
    pip install requests beautifulsoup4 json jq python-dotenv langchain_openai streamlit
    ```

## Téléchargement du code

Dans votre dossier, vous pouvez cloner le code en utilisant la commande suivante :
```bash
git clone https://github.com/Pasise/Challenge354

```
Une fois le code téléchargé, vous pouvez accéder au dossier Challenge354/Rendu en utilisant la commande suivante :
```bash
cd Challenge354/Rendu
```
## Fichier .env
Pour utiliser le chatbot, vous devez créer un fichier .env dans lequel vous allez mettre votre clé API OpenAI. 
Vous mettrez la clé dans la variable d'environnement OPENAI_API_KEY du fichier.env 

# Contenu du dossier

Le dossier contient les fichiers suivants:
- **scraping.py** : Ce fichier contient le code pour le web scraping des articles.
- **embeddings.py** : Ce fichier contient le code pour le stockage des données en vecteur. Le dossier faiss_index2 sera créé et contiendra 2 fichiers : index.faiss et index.pkl qui respectivement contiennent les données en vecteur et les métadonnées.
- **chatbot.py** : Ce fichier contient le code pour l'implémentation du RAG.
- **extracted_data.json** : Ce fichier contient les données extraites des articles.
- Le dossier faiss_index2 : Ce dossier contient les données en vecteur et leurs métadonnées.
- L'image robot2.png : Cette image est utilisée pour l'interface graphique

# Exécution du code

Afin d'exécuter le code, vous avez 2 possibilités :
- La première est juste d'appeler le chatbot en utilisant la commande suivante dans votre terminal :
  ```
  streamlit run chatbot.py
  ```

- La deuxième option, si vous voulez observer les différentes étapes de scraping, la création du fichier JSON, le stockage de ces données en vecteur et l'implémentation du RAG, vous pouvez exécuter les commandes suivantes dans votre terminal :
- Pour le scraping : 
  ```
  python scraping.py
  ```
  Vous aurez un fichier JSON qui sera créé.
- Pour le stockage des données en vecteur : 
  ```
  python3 embeddings.py
  ```
- Pour lancer le chatbot : 
  ```
  streamlit run chatbot.py
  ```

# Comment sont stockées les données ? 

- Les données sont extraites de la page htlm du site et stockées dans un fichier JSON.Les 25 premières pages ont été extraites nous données des articles publiées entre le 27/05/2024 et 02/06/2024. Mais en relancant le script scraping.py vous aurez des artcles plus récents. On recupère:
    - le titre
    - l'url de l'article
    - le contenu de l'article
    - la date de publication
    - la catégorie de l'article(Agro,Finance...)
- Ensuite, elles sont stockées en vecteur dans un fichier faiss. Les métadonnées sont stockées dans un fichier pkl. Porcéder de cette manière offre une combinaison d'efficacité de stockage, de rapidité d'accès aux données et de facilité d'organisation, ce qui est bénéfique pour le processus RAG et les opérations associées de traitement de texte

# Comment fonctionne le chatbot ?
Ce code implémente un chatbot pour le site Ecofin en utilisant des techniques de traitement du langage naturel . Voici un résumé des étapes clés :

1. **Initialisation du chatbot** : Le code utilise les bibliothèques `langchain_openai` et `langchain_community` pour créer un chatbot alimenté par GPT-3.5 et une chaîne de récupération conversationnelle.

2. **Interrogation du chatbot** : L'utilisateur peut saisir une question liée aux articles dans l'interface utilisateur (UI) créée avec Streamlit. La question est envoyée à la fonction `query` qui traite la question et renvoie une réponse.

3. **Traitement de la requête** : La fonction `query` charge une base de données locale Faiss contenant des vecteurs d'incorporation (embeddings) de données provenant du site web. En utilisant ces vecteurs et l'historique de la conversation, une réponse est générée à partir du modèle GPT-3.5.

4. **Affichage des résultats** : La réponse du chatbot est affichée dans l'interface utilisateur, et l'historique de la conversation est conservé pour les interactions futures.


# Exemples de questions à poser au chatbot
- Quels sont les articles les plus récents ?
- Quels sont les articles sur l'agriculture ?
- Quels sont les articles sur la finance ?
- Que s'est il passé au TOGO récemment? (ou un autre pays d'Afrique)
- Quels articles ont été plubliés le 01 Juin? 
