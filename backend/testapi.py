"""
Script de test de l'API d'authentification
Teste l'inscription, la connexion et l'accès aux ressources protégées
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_register():
    """Test d'inscription"""
    print("\n🧪 Test 1: Inscription d'un nouvel utilisateur")

    url = f"{BASE_URL}/register"
    data = {
        "nom": "Test",
        "prenom": "User",
        "email": "test.user@example.com",
        "password": "testpass123",
        "departement_id": 1,
        "groupe_id": 3,  # Eleve
    }

    response = requests.post(url, json=data)

    if response.status_code == 201:
        print("✅ Inscription réussie!")
        print(json.dumps(response.json(), indent=2))
        return True
    elif response.status_code == 400:
        print("⚠️  Email déjà enregistré")
        return False
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return False


def test_login(email="admin@library.com", password="admin123"):
    """Test de connexion"""
    print(f"\n🧪 Test 2: Connexion avec {email}")

    url = f"{BASE_URL}/login"
    data = {"username": email, "password": password}

    response = requests.post(url, data=data)

    if response.status_code == 200:
        token_data = response.json()
        print("✅ Connexion réussie!")
        print(f"Token type: {token_data['token_type']}")
        print(f"Access token: {token_data['access_token'][:50]}...")
        return token_data["access_token"]
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return None


def test_me(token):
    """Test de récupération des infos utilisateur"""
    print("\n🧪 Test 3: Récupération des informations utilisateur (/me)")

    url = f"{BASE_URL}/me"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ Informations récupérées!")
        print(json.dumps(response.json(), indent=2))
        return True
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return False


def test_protected_route(token):
    """Test d'accès à une route protégée"""
    print("\n🧪 Test 4: Accès à une route protégée (liste des livres)")

    url = f"{BASE_URL}/livres/"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ Accès autorisé!")
        livres = response.json()
        print(f"Nombre de livres: {len(livres)}")
        return True
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return False


def test_create_departement(token):
    """Test de création d'un département (nécessite rôle Bibliothecaire)"""
    print("\n🧪 Test 5: Création d'un département (nécessite rôle Bibliothecaire)")

    url = f"{BASE_URL}/departements/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"nom": "Test Département"}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ Département créé!")
        print(json.dumps(response.json(), indent=2))
        return True
    elif response.status_code == 403:
        print(
            "⚠️  Accès refusé - permissions insuffisantes (normal si pas Bibliothecaire)"
        )
        return False
    elif response.status_code == 400:
        print("⚠️  Département existe déjà")
        return False
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return False


def test_invalid_token():
    """Test avec un token invalide"""
    print("\n🧪 Test 6: Accès avec un token invalide")

    url = f"{BASE_URL}/me"
    headers = {"Authorization": "Bearer invalid_token_here"}

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        print("✅ Rejet correct du token invalide!")
        return True
    else:
        print(f"❌ Comportement inattendu: {response.status_code}")
        return False


def main():
    """Lance tous les tests"""
    print("=" * 60)
    print("🧪 TESTS DE L'API D'AUTHENTIFICATION")
    print("=" * 60)

    # Test 1: Inscription
    test_register()

    # Test 2: Connexion avec admin
    token = test_login("admin@library.com", "admin123")

    if token:
        # Test 3: Récupération des infos
        test_me(token)

        # Test 4: Route protégée
        test_protected_route(token)

        # Test 5: Création (avec permissions)
        test_create_departement(token)

    # Test 6: Token invalide
    test_invalid_token()

    print("\n" + "=" * 60)
    print("✅ Tests terminés!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que l'API est lancée sur http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
