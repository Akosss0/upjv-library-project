# Système de Gestion de Bibliothèque Universitaire

> Application full-stack de gestion de bibliothèque avec système d'authentification, gestion des emprunts et notifications automatiques.

    - Clément DUBERSEUIL
    - Arthur JACQUOT
    - Julian CAZIN

---

## Vue d'ensemble

Système complet de gestion de bibliothèque universitaire permettant :
- La gestion du catalogue de livres et exemplaires
- Le suivi des emprunts et retours
- Un système de notifications automatiques (rappels J-30, J-5, retards)
- Une gestion des utilisateurs avec contrôle d'accès basé sur les rôles (RBAC)

**Rôles utilisateurs** :
- 👨‍💼 **Bibliothécaire** : Accès complet (gestion livres, emprunts, utilisateurs)
- 👨‍🏫 **Professeur** : Gestion des utilisateurs, consultation
- 👨‍🎓 **Élève** : Consultation du catalogue, gestion de ses emprunts

---

## Fonctionnalités

### 🔐 Authentification & Autorisation
- [x] Inscription et connexion avec JWT
- [x] Contrôle d'accès basé sur les rôles (RBAC)
- [x] Hashage sécurisé des mots de passe (bcrypt)
- [x] Tokens d'accès avec expiration (30 min)

### 📚 Gestion du Catalogue
- [x] CRUD complet pour les livres
- [x] Gestion des exemplaires et de leur état
- [x] Catégorisation des livres
- [ ] Recherche et filtrage avancés _(TODO: Frontend)_

### 📖 Gestion des Emprunts
- [x] Création et suivi des emprunts
- [x] Gestion des retours
- [x] Historique des emprunts
- [x] Statuts d'emprunt (En cours, Rendu, En retard)

### 📬 Système de Notifications
- [x] Rappels automatiques J-30 avant échéance
- [x] Rappels automatiques J-5 avant échéance
- [x] Détection des retards
- [x] Notifications personnalisées par utilisateur
- [ ] Envoi d'emails automatiques _(TODO)_

### 👥 Gestion des Utilisateurs
- [x] CRUD utilisateurs
- [x] Affectation de groupes et départements
- [x] Consultation des emprunts par utilisateur

---

## 🏗️ Architecture

```
upjv-library-project/
├── backend/                    # API REST FastAPI
│   ├── app/
│   │   ├── main.py            # Point d'entrée, routes
│   │   ├── models.py          # Modèles SQLAlchemy (ORM)
│   │   ├── schemas.py         # Schémas Pydantic (validation)
│   │   ├── database.py        # Configuration DB
│   │   ├── utils.py           # Fonctions utilitaires (hashage)
│   │   └── notifications.py   # Logique notifications
│   ├── mysql_data/            # Données MySQL (volumes Docker)
│   ├── docker-compose.yml     # Services Docker (API + MySQL)
│   ├── Dockerfile             # Image Docker backend
│   ├── requirements.txt       # Dépendances Python
│   ├── init_db.py             # Script d'initialisation DB
│   ├── test_backend.py        # Tests API (CRUD + RBAC)
│   └── test_notifications.py  # Tests notifications
│
├── frontend/                   # Application React
│   ├── frontend/              # Code source React
│   │   └── react/             # Composants React
│   ├── docker-compose.yml     # Service frontend
│   ├── Dockerfile             # Image Docker frontend
│   └── nginx.conf             # Configuration Nginx
│
├── .github/
│   └── workflows/
│       └── test-api.yml       # CI/CD GitHub Actions
│
├── Documentation_technique.pdf
├── Maquette.pdf
├── Plan_de_test_biblio.xlsx
└── README.md                  # Ce fichier
```

---

### DevOps
- **Docker** & **Docker Compose** : Containerisation
- **GitHub Actions** : CI/CD automatisé
- **Git** : Versioning

---

## 🚀 Installation

### Prérequis

- [Docker](https://www.docker.com/get-started) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)
- [Git](https://git-scm.com/)
- _(Pour développement local)_ Python 3.11+ et Node.js 18+

### Cloner le projet

```bash
git clone https://github.com/Akosss0/upjv-library-project.git
cd upjv-library-project
```

---

## ⚙️ Configuration

### Backend

1. **Créer le fichier `.env`** dans le dossier `backend/` :

```bash
cd backend
cp .env.example .env
```

2. **Modifier les variables** dans `.env` :

```env
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=*


DB_USER=lib
DB_PASSWORD=
DB_ROOT_PASSWORD=
DB_HOST=db
DB_DATABASE=bibliotheque
DB_PORT=3306
```

### .env


```env
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=*


DB_USER=lib
DB_PASSWORD=
DB_ROOT_PASSWORD=
DB_HOST=db
DB_DATABASE=bibliotheque
DB_PORT=3306
```

---

## 💻 Utilisation

### Démarrage rapide (Docker)

#### Backend + Base de données

```bash
cd backend
docker compose up -d
```

L'API sera accessible sur : **http://localhost/api**

**Endpoints importants** :
- 📖 Documentation Swagger : http://localhost/api/docs


### Compte administrateur par défaut

```
Email: admin@library.com
Mot de passe: admin123
```

⚠️ **IMPORTANT** : Changez ce mot de passe en production !



## 📚 API Documentation

### Authentification

```bash
# Inscription
curl -X POST http://localhost/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "password": "motdepasse123",
    "departement_id": 1,
    "groupe_id": 3
  }'

# Connexion
curl -X POST http://localhost/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@library.com",
    "password": "admin123"
  }'

# Réponse: {"access_token": "eyJ...", "token_type": "bearer"}
```

### Utilisation du token

```bash
# Utiliser le token pour accéder aux routes protégées
curl http://localhost/api/livres/ \
  -H "Authorization: Bearer VOTRE_TOKEN"
```

### Routes principales

| Méthode | Endpoint | Permission | Description |
|---------|----------|------------|-------------|
| **Auth** ||||
| POST | `/register` | Public | Inscription |
| POST | `/login` | Public | Connexion |
| GET | `/me` | Authentifié | Profil utilisateur |
| **Livres** ||||
| GET | `/livres/` | Public | Liste des livres |
| POST | `/livres/` | Bibliothécaire | Créer un livre |
| GET | `/livres/{id}` | Public | Détails d'un livre |
| PUT/PATCH | `/livres/{id}` | Bibliothécaire | Modifier un livre |
| DELETE | `/livres/{id}` | Bibliothécaire | Supprimer un livre |
| **Emprunts** ||||
| GET | `/emprunts/` | Public | Liste des emprunts |
| POST | `/emprunts/` | Bibliothécaire | Créer un emprunt |
| **Notifications** ||||
| GET | `/notifications/retards` | Bibliothécaire | Emprunts en retard |
| GET | `/notifications/rappels/j30` | Bibliothécaire | Rappels J-30 |
| GET | `/notifications/rappels/j5` | Bibliothécaire | Rappels J-5 |
| GET | `/notifications/mes-notifications` | Authentifié | Mes notifications |

**Documentation complète** : http://localhost/api/docs

---

## 🧪 Tests

### Tests automatisés

Le projet inclut une suite complète de tests automatisés :

#### Backend

```bash
cd backend

# Tests CRUD + RBAC (Plan Excel)
python test_backend.py

# Tests système de notifications
python test_notifications.py

```

**Résultats attendus** :
- ✅ 58 tests CRUD (Plan Excel)
- ✅ 13 tests Bonus
- ✅ 9 tests Notifications
- **Total : 80 tests**


## 🌐 Déploiement

### Production avec Docker

```bash
# 1. Cloner sur le serveur
git clone https://github.com/Akosss0/upjv-library-project.git
cd upjv-library-project

# 2. Configurer les variables d'environnement
cd backend
nano .env  # Modifier avec des valeurs sécurisées

cd ..
nano .env  # si impossible de lancer le project sans alors le complete à l'aide du .env exemple
# 3. Lancer les services
docker compose up -d --build

# 4. Vérifier (peut prendre plusieurs minutes)
docker compose ps
curl http://localhost/api/docs
```


## 📖 Documentation

### Documentation technique

- 📄 [Documentation Technique](./Documentation_technique.pdf)
- 🎨 [Maquettes](./Maquette.pdf)
- 📊 [Plan de test](./Plan_de_test_biblio.xlsx)


### API

- Swagger UI : http://localhost:8000/docs

---

## Problèmes connus

### Backend

- [ ] Les rappels J-30 et J-5 sont calculés mais pas envoyés automatiquement (nécessite un cron/scheduler)
- [x] ~~Problème de hashage bcrypt~~ (résolu avec bcrypt==4.0.1)
- [x] ~~Swagger ne s'affiche pas~~ (résolu avec openapi_version="3.1.0")




## 👥 Auteurs

- **[BUT3 ALT]** - *Équipe de développement*
    - Clément DUBERSEUIL
    - Arthur JACQUOT
    - Julian CAZIN

---



