# Library Management API

API de gestion de bibliothèque avec authentification JWT et contrôle d'accès basé sur les rôles (RBAC).

## 🚀 Démarrage rapide

### 1. Configuration

Créez un fichier `.env` basé sur `.env.example` :

```bash
cp .env.example .env
```

Modifiez les valeurs dans `.env`, **surtout `SECRET_KEY`** pour la production.

### 2. Lancer l'application

```bash
docker-compose up --build -d
```

**🎉 C'est tout !** L'API sera disponible sur `http://localhost:8000`

La base de données sera **automatiquement initialisée** au premier lancement avec :
- Les groupes (Bibliothecaire, Professeur, Eleve)
- Les départements
- Les états, statuts, catégories
- Un utilisateur admin : `admin@library.com` / `admin123`

### 3. Documentation interactive

- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 🔄 **Fonctionnement automatique**

Au lancement (`docker-compose up`), le conteneur :
1. ✅ Attend que MySQL soit prêt (healthcheck)
2. ✅ Exécute automatiquement `init_db.py`
3. ✅ Lance l'API FastAPI

**Note** : Si vous relancez le conteneur, `init_db.py` vérifie que les données existent déjà et ne crée pas de doublons.

## 🔐 Authentification

### 1. Inscription (`/register`)

**POST** `http://localhost:8000/register`

```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "password": "motdepasse123",
  "departement_id": 1,
  "groupe_id": 3
}
```

**Réponse** (201 Created) :
```json
{
  "utilisateurs_id": 1,
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@example.com",
  "departement_id": 1,
  "groupe_id": 3
}
```

### 2. Connexion (`/login`) - Format JSON propre ✨

**POST** `http://localhost:8000/login`

Content-Type: `application/json`

```json
{
  "email": "admin@library.com",
  "password": "admin123"
}
```

**Réponse** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Exemple avec curl** :
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@library.com", "password": "admin123"}'
```

### 3. Utiliser le token

Dans les requêtes protégées, ajoutez le header :

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Exemple avec curl** :
```bash
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Récupérer ses informations (`/me`)

**GET** `http://localhost:8000/me`

Headers :
```
Authorization: Bearer YOUR_TOKEN
```

## 🔓 **Utiliser l'authentification dans Swagger**

### Méthode 1 : Via le bouton Authorize (recommandé)

1. Allez sur `http://localhost:8000/docs`
2. Cliquez sur **POST `/login`**
3. Cliquez sur "Try it out"
4. Entrez dans le corps JSON :
   ```json
   {
     "email": "admin@library.com",
     "password": "admin123"
   }
   ```
5. Exécutez et **copiez le `access_token`**
6. Cliquez sur le bouton **"Authorize" 🔒** (en haut à droite)
7. Collez le token (sans "Bearer", il sera ajouté automatiquement)
8. Cliquez sur "Authorize"
9. ✅ Toutes vos requêtes incluront maintenant le token automatiquement !

### Méthode 2 : Manuellement pour chaque requête

Pour chaque endpoint, dans le header `Authorization`, mettez :
```
Bearer YOUR_TOKEN
```

## 📋 Groupes et permissions

| Groupe | ID | Permissions |
|--------|-----|------------|
| **Bibliothecaire** | 1 | Toutes les opérations CRUD |
| **Professeur** | 2 | Gestion des utilisateurs |
| **Eleve** | 3 | Lecture uniquement (par défaut) |

## 🗂️ Structure de la base de données

Les données de référence sont créées automatiquement :

1. ✅ **Groupes** : Bibliothecaire, Professeur, Eleve
2. ✅ **Départements** : Informatique, Mathématiques, Physique, Chimie, Biologie, Histoire, Géographie
3. ✅ **États** : Neuf, Très bon, Bon, Acceptable, Abîmé, Très abîmé
4. ✅ **Statuts** : En cours, Rendu à temps, Rendu en retard, Perdu
5. ✅ **Catégories** : Roman, Science-fiction, Fantasy, Policier, Thriller, Histoire, Biographie, Science, etc.
6. ✅ **Admin** : admin@library.com / admin123

## 📝 Exemples d'utilisation

### Script de test automatique

Un script python est fourni pour tester rapidement l'API :

```bash
    cd ./backend/
    python ./test_backend.py
```

### Créer un département (Bibliothecaire requis)

```bash
curl -X POST http://localhost:8000/departements/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Langues"}'
```

### Créer un livre (Bibliothecaire requis)

```bash
curl -X POST http://localhost:8000/livres/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "1984",
    "auteur": "George Orwell",
    "categorie_id": 1,
    "isbn": "978-0451524935",
    "annee_publication": 1949,
    "editeur": "Penguin Books",
    "resume": "Dystopie sur un régime totalitaire"
  }'
```

### Lister les livres (accessible à tous)

```bash
curl http://localhost:8000/livres/
```

### S'inscrire

```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Martin",
    "prenom": "Sophie",
    "email": "sophie.martin@example.com",
    "password": "secure123",
    "departement_id": 1,
    "groupe_id": 3
  }'
```

## 🔧 Développement

### Structure des fichiers

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Routes et logique principale
│   ├── models.py        # Modèles SQLAlchemy
│   ├── schemas.py       # Schémas Pydantic
│   └── database.py      # Configuration DB
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── init_db.py          # Script d'initialisation
├── entrypoint.sh       # Script de démarrage
├── test_curl.sh        # Tests curl
└── .env                # Configuration (à créer)
```

### Commandes utiles

**Reconstruire et relancer** :
```bash
docker-compose up --build -d
```

**Arrêter l'application** :
```bash
docker-compose down
```

**Voir les logs** :
```bash
docker-compose logs -f backend
```

**Voir les logs MySQL** :
```bash
docker-compose logs -f db
```

**Réinitialiser complètement** (⚠️ supprime les données) :
```bash
docker-compose down -v
docker-compose up --build -d
```
et Supprimer le dossier mysql_data dans le backend

**Exécuter init_db.py manuellement** (si besoin) :
```bash
docker exec fastapi-backend python init_db.py
```

**Accéder au conteneur backend** :
```bash
docker exec -it fastapi-backend bash
```

**Accéder à MySQL** :
```bash
docker exec -it <container_id_mysql> mysql -u library_user -p library_db
```

## 🧪 Tests

### Script Python automatisé

```bash
pip install requests  # Si pas déjà installé
python test_api.py
```

### Script bash avec test

```bash
    ./test_backend.py
    ./test_backend.py
```

Les tests vérifient :
- ✅ Inscription
- ✅ Connexion (format JSON propre)
- ✅ Récupération des infos utilisateur
- ✅ Accès aux routes protégées
- ✅ Création avec permissions
- ✅ Rejet des tokens invalides

- ✅ Les notifications d'enmprunts

## ⚠️ Sécurité - Production

Pour la production, assurez-vous de :

1. ✅ Changer `SECRET_KEY` dans `.env` (minimum 32 caractères aléatoires)
   ```bash
   # Générer une clé sécurisée :
   openssl rand -hex 32
   ```
2. ✅ Utiliser des mots de passe forts pour la base de données
3. ✅ Activer HTTPS
4. ✅ Limiter les taux de requêtes (rate limiting)
5. ✅ Configurer CORS correctement si nécessaire
6. ✅ Changer le mot de passe admin par défaut
7. ✅ Ajouter une politique de mots de passe forts
8. ✅ Ajouter une durée d'expiration appropriée pour les tokens

## 🆕 Nouveautés

### Format de login propre
- ✨ Login avec JSON `{"email": "...", "password": "..."}` au lieu du format form-data
- 🔒 Bouton "Authorize" dans Swagger avec champ Bearer token simple
- 📝 Documentation et exemples plus clairs

## 📚 Ressources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [JWT.io](https://jwt.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [HTTPBearer Security](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)