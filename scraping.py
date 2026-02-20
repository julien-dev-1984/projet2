# Utilisation de la bibliothèque requests pour récupérer l'url de la page web
import requests
from bs4 import BeautifulSoup


url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(url)


soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify())