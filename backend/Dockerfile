FROM python:3.11-slim

WORKDIR /code

# Copier et installer les dépendances
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copier le code de l'application
COPY ./app /code/app

# Copier le script d'initialisation
COPY ./initdb.py /code/init_db.py

# Copier le script d'entrée
COPY ./entrypoint.sh /code/entrypoint.sh

# Rendre le script exécutable
RUN chmod +x /code/entrypoint.sh

# Utiliser le script d'entrée comme commande
CMD ["/code/entrypoint.sh"]