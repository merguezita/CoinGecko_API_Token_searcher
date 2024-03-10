import requests
import json
import time

def get_crypto_list_with_AI():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    #print(response.json())
    if response.status_code == 200:
        crypto_list = response.json()
        crypto_with_AI = [crypto for crypto in crypto_list if 'ai' in crypto['name'].lower() or 'ia' in crypto['name'].lower()]
        return crypto_with_AI
    else:
        print("Erreur lors de la récupération de la liste des crypto-monnaies l13")
        return []

def get_crypto_details(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    response = requests.get(url)
    if response.status_code == 200:
        crypto_data = response.json()
        
        # Conditions de filtrage
        if ('dai' or 'aave' or 'chain' ) in crypto_data['name'].lower():
            return None
        
        market_data = crypto_data.get('market_data', {})
        total_volume = market_data.get('total_volume', {})
        
        if total_volume.get('usd', 0) == 0:
            return None
        
        return {
            'name': crypto_data['name'],
            'symbol': crypto_data['symbol'],
            'market_cap': market_data.get('market_cap', {}).get('usd', ''),
            'current_price': market_data.get('current_price', {}).get('usd', ''),
            'total_supply': market_data.get('total_supply', ''),
            'circulating_supply': market_data.get('circulating_supply', ''),
            'website': crypto_data.get('links', {}).get('homepage', [])[0] if crypto_data.get('links', {}) else None,
            'volume_24h': total_volume.get('usd', ''),
            'twitter_followers': crypto_data.get('community_data', {}).get('twitter_followers', None)
        }
    else:
        print(f"Erreur lors de la récupération des détails pour {crypto_id}")
        return None

def main():
    ai_crypto_names = []  # Liste pour stocker les noms des cryptos contenant "AI"
    
    with open('ai_crypto_CoinGecko.txt', 'w', encoding='utf-8') as names_file:
        # Écrire un message d'en-tête dans le fichier
        names_file.write("Liste des cryptos contenant 'AI':\n\n")

        crypto_list_with_AI = get_crypto_list_with_AI()
        for crypto in crypto_list_with_AI:
            ai_crypto_names.append(crypto['name'])  # Ajouter le nom de la crypto à la liste
            names_file.write(crypto['name'] + "\n")  # Écrire le nom de la crypto dans le fichier

        print(f"Nombre total de cryptos contenant 'AI': {len(ai_crypto_names)}")
    
    output_data = []
    for crypto in crypto_list_with_AI:
        crypto_details = get_crypto_details(crypto['id'])
        if crypto_details:
            output_data.append(crypto_details)
            print("Nom:", crypto_details['name'])
            print("Symbole:", crypto_details['symbol'])
            print("Capitalisation boursière:", crypto_details['market_cap'])
            print("Prix actuel:", crypto_details['current_price'])
            print("Offre totale:", crypto_details['total_supply'])
            print("Offre en circulation:", crypto_details['circulating_supply'])
            print("Site internet associé:", crypto_details['website'])
            print("Volume de négociation sur 24 heures:", crypto_details['volume_24h'])
            print("Nombre de followers Twitter:", crypto_details['twitter_followers'])
            print("-" * 50)
        time.sleep(12)  # Attendre 12 secondes entre chaque requête pour ne dépasser le quota de l'API
    with open('crypto_data_CoinGecko.json', 'w', encoding='utf-8') as json_file: #Nom du fichier final format .json
        json.dump(output_data, json_file, indent=4)

if __name__ == "__main__":
    main()
