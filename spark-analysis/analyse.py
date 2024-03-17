import boto3
from io import BytesIO
import time
from database import add_player_stats
from database import create_or_update_table, add_player_stats
import pandas as pd
import datetime

from sqlalchemy.orm import sessionmaker

# Remplacez ces valeurs par les informations de votre serveur MinIO
minio_endpoint = "http://minio:9000"
minio_access_key = "votre-access-key"
minio_secret_key = "votre-secret-key"

# Remplacez ces valeurs par le nom de votre bucket et le chemin objet dans S3
bucket_name = "football"
s3_object_key = "data.csv"

# df = pd.read_csv("players_stats.csv")


def calculs(row):
    duels_rate = (row["DuelsWon"] / row["DuelsTotal"]) * 100
    match_goal_assist_ratio = row["Minutes"] / (row["Assists"] + row["GoalsTotal"])
    average_time_ga = (row["Assists"] + row["GoalsTotal"]) / row["Minutes"]
    dribble_rate = row["DribblesSuccess"] / row["DribblesAttempts"]

    return pd.Series(
        {
            "duels_rate": duels_rate,
            "match_goal_assist_ratio": match_goal_assist_ratio,
            "average_time_ga": average_time_ga,
            "dribble_rate": dribble_rate,
        }
    )


# Fonction pour récupérer le fichier depuis MinIO
def get_file_from_minio():
    s3_client = boto3.client(
        "s3",
        endpoint_url=minio_endpoint,
        aws_access_key_id=minio_access_key,
        aws_secret_access_key=minio_secret_key,
    )

    # Télécharger le fichier depuis MinIO
    obj = s3_client.get_object(Bucket=bucket_name, Key=s3_object_key)
    data = obj["Body"].read()

    df = pd.read_csv(BytesIO(data))

    return df


if __name__ == "__main__":
    while True:
        time.sleep(15)

        df = get_file_from_minio()
        resultats = df.apply(calculs, axis=1)
        df = pd.concat([df, resultats], axis=1)
        print(df)
        # Créer ou mettre à jour la table dans la base de données
        engine = create_or_update_table()

        # Récupérer le fichier depuis MinIO
        # get_file_from_minio()
        Session = sessionmaker(bind=engine)
        session = Session()

        # Ajouter chaque ligne dans la base de données
        for index, row in df.iterrows():
            data = {
                "appearences": row["Appearances"],
                "lineups": row["Lineups"],
                "minutes": row["Minutes"],
                "rating": row["Rating"],
                "total_shots": row["ShotsTotal"],
                "on_target_shots": row["ShotsOnTarget"],
                "total_goals": row["GoalsTotal"],
                "assists": row["Assists"],
                "total_passes": row["PassesTotal"],
                "key_passes": row["PassesKey"],
                "total_duels": row["DuelsTotal"],
                "duels_won": row["DuelsWon"],
                "dribble_attempts": row["DribblesAttempts"],
                "successful_dribbles": row["DribblesSuccess"],
                "penalty_scored": row["PenaltyScored"],
                "penalty_missed": row["PenaltyMissed"],
                "registred_date": datetime.datetime.now(),
                "player_id": row["PlayerId"],
                "duels_rate": row["duels_rate"],
                "match_goal_assist_ratio": row["match_goal_assist_ratio"],
                "average_time_ga": row["average_time_ga"],
                "dribble_rate": row["dribble_rate"],
                "firstname": row["PlayerFirstname"],
                "lastname": row["PlayerLastname"],
            }
            add_player_stats(session, data)

        # Fermer la session
        session.close()
        time.sleep(24 * 60 * 60 + 15)
