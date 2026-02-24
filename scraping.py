import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)

if response.status_code != 200:
    print("Erreur requête :", response.status_code)
    raise SystemExit

soup = BeautifulSoup(response.text, "html.parser")

upc = soup.find("th", string="UPC").find_next_sibling("td").get_text(strip=True)
title = soup.find("h1").get_text(strip=True)

price_incl_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").get_text(strip=True)
price_excl_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").get_text(strip=True)

stock_text = soup.find("th", string="Availability").find_next_sibling("td").get_text(" ", strip=True)
m = re.search(r"(\d+)", stock_text)
number_available = m.group(1) if m else ""

desc_tag = soup.find("div", id="product_description")
product_description = desc_tag.find_next_sibling("p").get_text(strip=True) if desc_tag else ""

category = soup.find("ul", class_="breadcrumb").find_all("li")[2].get_text(strip=True)
review_rating = soup.find("p", class_="star-rating")["class"][1]

image_rel = soup.find("div", class_="item active").find("img")["src"]
image_url = image_rel.replace("../../", "https://books.toscrape.com/")

# Nettoyage prix
price_incl_tax = price_incl_tax.replace("£", "").replace("Â", "").strip()
price_excl_tax = price_excl_tax.replace("£", "").replace("Â", "").strip()

donnees_livre = {
    "product_page_url": url,
    "universal_product_code (upc)": upc,
    "title": title,
    "price_including_tax": price_incl_tax,
    "price_excluding_tax": price_excl_tax,
    "number_available": number_available,
    "product_description": product_description,
    "category": category,
    "review_rating": review_rating,
    "image_url": image_url,
}

filename = f"livre_{title[:20].replace(' ', '_')}_scrap.csv"

with open(filename, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=donnees_livre.keys(), delimiter=",")
    writer.writeheader()
    writer.writerow(donnees_livre)

print("Données extraites ! Fichier :", filename)
print("Aperçu :", donnees_livre)