import requests
import json
import pandas as pd
import subprocess
from s3 import upload_to_minio
import time
from os import getenv


# Fonction pour récupérer les statistiques d'un joueur depuis l'API
def get_player_stats(player_id, season):
    api_url = f"https://{getenv('API_HOST')}/v3/players?id={player_id}&season={season}"
    headers = {
        "x-rapidapi-host": getenv("API_HOST"),
        "x-rapidapi-key": getenv("API_KEY"),  # Remplacez par votre clé API
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        print(list(data["response"]))
        return list(data["response"])
    else:
        print(f"Erreur lors de la requête API : {data}")
        return None


def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête API : {e}")
        return None


def convert_json_to_csv(player_stats_list):
    all_players_data = []

    for player_stats in player_stats_list:
        # Extraire les données nécessaires du JSON
        data = {
            "Appearances": player_stats[0]["statistics"][0]["games"]["appearences"],
            "Lineups": player_stats[0]["statistics"][0]["games"]["lineups"],
            "Minutes": player_stats[0]["statistics"][0]["games"]["minutes"],
            "Rating": player_stats[0]["statistics"][0]["games"]["rating"],
            "ShotsTotal": player_stats[0]["statistics"][0]["shots"]["total"],
            "ShotsOnTarget": player_stats[0]["statistics"][0]["shots"]["on"],
            "GoalsTotal": player_stats[0]["statistics"][0]["goals"]["total"],
            "Assists": player_stats[0]["statistics"][0]["goals"]["assists"],
            "PassesTotal": player_stats[0]["statistics"][0]["passes"]["total"],
            "PassesKey": player_stats[0]["statistics"][0]["passes"]["key"],
            "DuelsTotal": player_stats[0]["statistics"][0]["duels"]["total"],
            "DuelsWon": player_stats[0]["statistics"][0]["duels"]["won"],
            "DribblesAttempts": player_stats[0]["statistics"][0]["dribbles"][
                "attempts"
            ],
            "DribblesSuccess": player_stats[0]["statistics"][0]["dribbles"]["success"],
            "PenaltyScored": player_stats[0]["statistics"][0]["penalty"]["scored"],
            "PenaltyMissed": player_stats[0]["statistics"][0]["penalty"]["missed"],
            "PlayerId": player_stats[0]["player"]["id"],
            "PlayerFirstname": player_stats[0]["player"]["firstname"],
            "PlayerLastname": player_stats[0]["player"]["lastname"],
        }
        # Ajouter les données du joueur à la liste
        all_players_data.append(data)

    # Créer un DataFrame Pandas à partir des données
    df = pd.DataFrame(all_players_data)

    # Écrire le DataFrame dans un fichier CSV
    df.to_csv("players_stats.csv", index=False)


# Exemple d'utilisation
if __name__ == "__main__":
    while True:
        player_ids = [1100, 184]  # Liste d'identifiants de joueurs
        season = "2023"

        # Liste pour stocker les statistiques de chaque joueur
        all_player_stats = []

        # Récupérer les statistiques pour chaque joueur
        for player_id in player_ids:
            player_stats = get_player_stats(player_id, season)
            if player_stats:
                all_player_stats.append(player_stats)

        # Convertir les données en CSV
        convert_json_to_csv(all_player_stats)
        # Utiliser la fonction d'upload vers S3
        file_path = "players_stats.csv"
        bucket_name = "football"
        object_name = "data.csv"
        minio_url = "http://minio:9000"
        access_key = "votre-access-key"
        secret_key = "votre-secret-key"

        upload_to_minio(
            file_path, bucket_name, object_name, minio_url, access_key, secret_key
        )
        # Attendre 24 heures avant la prochaine exécution
        time.sleep(24 * 60 * 60)  # 24 heures en secondes
