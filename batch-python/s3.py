import boto3
from botocore.exceptions import NoCredentialsError
import json


def create_bucket_if_not_exists(s3, bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
    except s3.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            s3.create_bucket(Bucket=bucket_name)
            print(f"Le bucket {bucket_name} a été créé avec succès.")
        else:
            raise


def upload_to_minio(
    file_path, bucket_name, object_name, minio_url, access_key, secret_key
):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=minio_url,
    )

    create_bucket_if_not_exists(s3, bucket_name)

    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(
            f"Le fichier {file_path} a été uploadé avec succès vers {bucket_name}/{object_name} sur Minio."
        )
    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
    except NoCredentialsError:
        print(
            "Les informations d'identification AWS ne sont pas configurées correctement ou sont manquantes."
        )


# Exemple d'utilisation
file_path = "./data.json"
bucket_name = "football"
object_name = "pasrien.json"
minio_url = "http://localhost:9000"
access_key = "votre-access-key"
secret_key = "votre-secret-key"

# upload_to_minio(file_path, bucket_name, object_name, minio_url, access_key, secret_key)
