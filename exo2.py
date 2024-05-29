import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de base
base_url = "https://quotes.toscrape.com"
login_url = f"{base_url}/login"
page_url = f"{base_url}/tag/books/page/{{}}/"

# Informations de connexion
login_data = {
    'username': 'test',
    'password': 'test'
}

# Session pour maintenir la connexion
session = requests.Session()
response = session.post(login_url, data=login_data)

# Récupérer le token de la réponse
token = response.cookies.get('session')

# Lire le fichier CSV existant
df = pd.read_csv('results.csv')

# Ajouter une colonne pour le token
df['Token'] = token

# Sauvegarder le DataFrame avec le token
df.to_csv('results.csv', index=False)

print("Le token a été ajouté à 'results.csv'.")

# Initialisation des listes pour stocker les données
quotes = []
tags = []

# Récupérer les citations des pages 1 et 2 avec le tag 'books'
for page in range(1, 3):
    response = session.get(page_url.format(page))
    soup = BeautifulSoup(response.content, 'html.parser')

    for quote in soup.find_all('div', class_='quote'):
        quote_tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        if 'books' in quote_tags:
            quotes.append(quote.find('span', class_='text').get_text())
            tags.append(", ".join(quote_tags))

# Création d'un DataFrame pour les nouvelles citations
new_df = pd.DataFrame({
    'Quote': quotes,
    'Tags': tags
})

# Fusionner avec le DataFrame existant et supprimer les doublons
combined_df = pd.concat([df, new_df]).drop_duplicates(subset=['Quote'])

# Sauvegarder le DataFrame combiné sans doublons
combined_df.to_csv('results.csv', index=False)

print("Les nouvelles citations ont été ajoutées et les doublons ont été supprimés.")
