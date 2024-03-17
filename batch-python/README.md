# Batch Python

Batch en python qui récupère des données de l'api

## TODO

- [ ] Créer un fichier qui fait un batch sur nos deux joueurs (Haaland et kane)
- [ ] modifier les fichier pour mettre les bons champs de connexion à la base
- [ ] Dockerfile + docker-compose pour tester

## structure

`database.py`:  créer ou update la structure de la table (à modifier)

`update-database.py`: update les stats des joueurs (à modifier)

## Dev

* interface avec hdfs: [hdfscli.readthedocs.io](https://hdfscli.readthedocs.io/en/latest/)

* Interface avec l'api: [urllib3.readthedocs.io](https://urllib3.readthedocs.io/en/stable/user-guide.html)

* Faire un job periodique: [asyncio](https://www.slingacademy.com/article/python-running-a-function-periodically-with-asyncio/)