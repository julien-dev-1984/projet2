import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html"
response = requests.get(url)
response.encoding = "utf-8"

if response.status_code != 200:
    print("Erreur :", response.status_code)
else:
    soup = BeautifulSoup(response.text, "html.parser")

    upc = soup.find("th", string="UPC").find_next_sibling("td").get_text(strip=True)
    title = soup.find("h1").get_text()
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").get_text(strip=True)
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").get_text(strip=True)
    number_available = soup.find("th", string="Availability").find_next_sibling("td").get_text(strip=True)
    product_description = soup.find("div", id="product_description").find_next_sibling("p").get_text(strip=True)
    category = soup.select("ul.breadcrumb li a")[-1].get_text(strip=True)
    review_rating = soup.find("p", class_="star-rating")["class"][1]
    image_rel = soup.find("div", class_="item active").find("img")["src"]
    image_url = image_rel.replace("../../", "https://books.toscrape.com/")

    donnees_livre = {
        "upc": upc,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }

    print(donnees_livre)

    filename = f"{title[:30].replace(' ', '_').replace(':', '')}.csv"

    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=donnees_livre.keys())
        writer.writeheader()
        writer.writerow(donnees_livre)

print(f"Données extraites et enregistrées dans {filename}")
