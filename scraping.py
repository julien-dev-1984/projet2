# Utilisation de la bibliothèque requests pour récupérer l'url de la page web
import requests

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Simulation du navigateur web utilisé pour éviter d'être bloqué par le site web
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("La page a été récupérée avec succès !")
    # Affichage du contenu de la page web
    html_content = response.text

    # Affichage du contenu de la page web
    print(html_content)

else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")