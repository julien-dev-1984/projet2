# Utilisation de la bibliothèque requests pour récupérer l'url de la page web
import requests
# Utilisation de la bibliothèque BeautifulSoup pour parser le contenu HTML de la page web
from bs4 import BeautifulSoup
# Utilisation de la bibliothèque csv pour écrire les données extraites dans un fichier CSV
import csv


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Récupération du contenu de la page web
response = requests.get(url)

# Vérification que la requête a réussi
if response.status_code == 200:

# Extraction des données de la page web à l'aide de BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    upc = soup.find("th", string="UPC").find_next_sibling("td").text
    title = soup.find("h1").text
    price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").text
    price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").text
    stock_book = soup.find("th", string="Availability").find_next_sibling("td").text.strip()
    number_available = stock_book.split(" ")[2]  # Extrait le nombre de livres disponibles
    product_description = soup.find("div", id="product_description").find_next_sibling("p").text
    category = soup.find("ul", class_="breadcrumb").find_all("li")[2].text.strip()
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_url = soup.find("div", class_="item active").find("img")["src"]
    image_url = image_url.replace("../../", "https://books.toscrape.com/")

if response.status_code == 200:

    # Nettoyage des prix pour enlever le symbole £ et les résidus d'encodage
    price_incl_tax = price_incl_tax.strip().replace("£", "").replace("Â", "")
    price_excl_tax = price_excl_tax.strip().replace("£", "").replace("Â", "")

    # Utilisation d'un dictionnaire pour stocker les données extraites
    donnees_livre = {
    "product_page_url": url,
    "universal_product_code (upc)": upc,
    "title": title,
    "price_including_tax": price_incl_tax,
    "price_excluding_tax": price_excl_tax,
    "number_available": stock_book,
    "product_description": product_description,
    "category": category,
    "review_rating": review_rating,
    "image_url": image_url
}

    en_tetes = list(donnees_livre.keys())

    # Nettoyage du stock pour n'avoir que le texte propre
    stock_book = stock_book.strip()

    # Écriture CSV (virgule, UTF-8 pour accents)
    filename = f"livre_{title[:20].replace(' ', '_')}_scrap.csv"  # Nom dynamique !
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=en_tetes, delimiter=",")  # Virgule !
        writer.writeheader()
        writer.writerow(donnees_livre)

    print(f"Données extraites ! Fichier : {filename}")
    print("Aperçu :", donnees_livre)
else:
        print(" Erreur requête :", response.status_code)