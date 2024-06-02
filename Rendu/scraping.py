import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def obtenir_url(): # Fonction pour obtenir les URL des pages
    urls = []
    numero_de_page = 0
    for i in range(25):
        url = f"https://www.agenceecofin.com/a-la-une/recherche-article/articles?submit_x=0&submit_y=0&filterTousLesFils=Tous&filterCategories=Sous-rubrique&filterFrench=French&userSearch=1&testlimitstart={numero_de_page}"
        numero_de_page += 7
        urls.append(url)
    return urls

def parser_page(url): # Fonction pour parser les pages
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    blocs = soup.find_all("tr")
    print(f"1")
   
    page_data = []
   
    for index, bloc in enumerate(blocs): # Boucle pour parcourir les blocs
        titre_tag = bloc.find('h3', class_='r')
        titre = titre_tag.text.strip() if titre_tag else "Titre non trouvé"

        lien = bloc.find("a", href=True) # Recherche du lien
        if lien:
            lien_href = lien['href'].strip()
        else:
            lien_href = "Lien non trouvé"

        description = bloc.find("div", class_="st") # Recherche de la description
        if description:
            description_text = description.text.strip()
        else:
            description_text = "Description non trouvée"

        date_tag = bloc.find("td", valign="top", class_="tsw") # Recherche de la date
        if date_tag:
            date_span = date_tag.find("div", class_="slp").find("span", class_="f nsa")
            date = date_span.text.strip() if date_span else "Date non trouvée"
        else:
            date = "Date non trouvée"

        categorie_tag = bloc.find("td", valign="top", class_="tsw") # Recherche de la catégorie
        if categorie_tag:
            categorie_span = categorie_tag.find("div", class_="slp").find("span", class_="news-source")
            categorie = categorie_span.text.strip() if categorie_span else "Categorie non trouvée"
        else:
            categorie = "Categorie non trouvée"

        article_data = {
            f"article": {
                "titre": titre,
                "href": lien_href,
                "description": description_text,
                "date de publication": date,
                "Categorie": categorie
            }
        }

        page_data.append(article_data)
    
    return page_data

def parser_les_pages(): #parser TOUTES les pages
    pages = obtenir_url()
    all_data = []
    for page in pages:
        page_data = parser_page(page)
        all_data.extend(page_data)
    
    data_dict = {"data": all_data}  # Ajout de la clé "data"
    
    with open('extracted_data.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

parser_les_pages()
