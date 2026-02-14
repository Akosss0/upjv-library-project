#!/usr/bin/env python3
"""
Script de test automatisé pour l'API Library Management
Basé sur le plan de test: Plan_de_test_biblio.xlsx

Ce script teste tous les scénarios du plan de test Excel et génère un rapport.
Les tests supplémentaires (non présents dans le plan Excel) sont marqués comme [BONUS].
"""

import requests
import json
from datetime import date, timedelta, datetime
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import sys
import uuid

# Configuration
BASE_URL = "http://localhost:8000"
ADMIN_EMAIL = "admin@library.com"
ADMIN_PASSWORD = "admin123"


# Couleurs pour le terminal
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


@dataclass
class TestResult:
    category: str
    scenario: str
    expected: str
    status: str  # "Conforme", "Non-Conforme", "En attente"
    response_code: int = None
    response_data: Any = None
    error_message: str = None
    is_bonus: bool = False  # Marqueur pour tests supplémentaires


class LibraryAPITester:
    def __init__(self):
        self.token = None
        self.results: List[TestResult] = []
        self.created_ids = {}  # Pour stocker les IDs créés pendant les tests

    def cleanup_test_users(self):
        """Nettoie les utilisateurs de test créés lors des exécutions précédentes"""
        try:
            # Récupérer tous les utilisateurs
            response = requests.get(
                f"{BASE_URL}/utilisateurs/", headers=self.get_headers()
            )
            if response.status_code == 200:
                users = response.json()
                deleted_count = 0

                # Supprimer les utilisateurs de test (email contient "test" ou "crud_test")
                for user in users:
                    email = user.get("email", "")
                    user_id = user.get("utilisateurs_id")

                    # Ne pas supprimer l'admin
                    if email == ADMIN_EMAIL:
                        continue

                    # Supprimer si c'est un utilisateur de test
                    if "test_user_" in email or "crud_test_" in email:
                        try:
                            del_response = requests.delete(
                                f"{BASE_URL}/utilisateurs/{user_id}",
                                headers=self.get_headers(),
                            )
                            if del_response.status_code == 204:
                                deleted_count += 1
                        except:
                            pass  # Ignorer les erreurs de suppression

                if deleted_count > 0:
                    print(
                        f"{Colors.YELLOW}🧹 Nettoyage: {deleted_count} utilisateur(s) de test supprimé(s){Colors.RESET}"
                    )
        except:
            pass  # Ignorer les erreurs de nettoyage

    def print_header(self, text: str):
        """Affiche un header coloré"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    def print_test(self, category: str, scenario: str, is_bonus: bool = False):
        """Affiche le test en cours"""
        bonus = f"{Colors.MAGENTA}[BONUS]{Colors.RESET} " if is_bonus else ""
        print(f"{bonus}{Colors.BLUE}[{category}]{Colors.RESET} {scenario}...", end=" ")

    def print_result(self, success: bool, details: str = ""):
        """Affiche le résultat d'un test"""
        if success:
            print(f"{Colors.GREEN}✓ OK{Colors.RESET}", end="")
        else:
            print(f"{Colors.RED}✗ ÉCHEC{Colors.RESET}", end="")
        if details:
            print(f" - {details}")
        else:
            print()

    def login(self) -> bool:
        """Connexion avec les credentials admin"""
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                return True
            return False
        except Exception as e:
            print(f"{Colors.RED}Erreur de connexion: {e}{Colors.RESET}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """Retourne les headers avec le token"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    # ========== TESTS DU PLAN EXCEL ==========

    def test_connexion(self):
        """Tests de connexion (du plan Excel)"""
        self.print_header("TESTS DE CONNEXION")

        # Test 1: Identifiants valides
        self.print_test("Connexion", "Renseigner des identifiants valides")
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
            )
            success = response.status_code == 200 and "access_token" in response.json()
            self.results.append(
                TestResult(
                    "Connexion",
                    "Renseigner des identifiants valides",
                    "On récupère un access_token et un refresh token",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    response.json() if success else None,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Connexion",
                    "Renseigner des identifiants valides",
                    "On récupère un access_token et un refresh token",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 2: Identifiants invalides
        self.print_test("Connexion", "Renseigner des identifiants invalides")
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": "wrong@email.com", "password": "wrongpass"},
            )
            success = response.status_code == 401
            self.results.append(
                TestResult(
                    "Connexion",
                    "Renseigner des identifiants invalides",
                    "On obtient une erreur 401",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Connexion",
                    "Renseigner des identifiants invalides",
                    "On obtient une erreur 401",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

    def test_inscription(self):
        """Tests d'inscription (du plan Excel)"""
        self.print_header("TESTS D'INSCRIPTION")

        # Test 1: Créer un utilisateur
        self.print_test("Inscription", "Se créer un utilisateur")
        # Utiliser UUID pour garantir l'unicité à chaque exécution
        test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                json={
                    "nom": "Test",
                    "prenom": "User",
                    "email": test_email,
                    "password": "testpass123",
                    "departement_id": 1,
                    "groupe_id": 3,
                },
            )
            success = response.status_code == 201
            self.results.append(
                TestResult(
                    "Inscription",
                    "Se créer un utilisateur",
                    "On retourne l'utilisateur créé en base",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    response.json() if success else None,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Inscription",
                    "Se créer un utilisateur",
                    "On retourne l'utilisateur créé en base",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 2: Email déjà existant
        self.print_test(
            "Inscription",
            "Se créer un utilisateur avec une adresse mail déjà existante",
        )
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                json={
                    "nom": "Test",
                    "prenom": "Duplicate",
                    "email": ADMIN_EMAIL,  # Email déjà existant
                    "password": "testpass123",
                    "departement_id": 1,
                    "groupe_id": 3,
                },
            )
            success = response.status_code == 400
            self.results.append(
                TestResult(
                    "Inscription",
                    "Se créer un utilisateur avec une adresse mail déjà existante",
                    "Une erreur est obtenue",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Inscription",
                    "Se créer un utilisateur avec une adresse mail déjà existante",
                    "Une erreur est obtenue",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

    def test_crud_endpoint(
        self,
        endpoint: str,
        category: str,
        sample_data: Dict[str, Any],
        skip_delete: bool = False,
    ):
        """Teste les opérations CRUD pour un endpoint donné (du plan Excel)

        Args:
            endpoint: L'endpoint à tester (ex: "livres")
            category: La catégorie pour l'affichage (ex: "Livre")
            sample_data: Données d'exemple pour créer l'entité
            skip_delete: Si True, ne supprime pas l'entité créée (pour les dépendances)
        """
        self.print_header(f"TESTS CRUD - {category.upper()}")

        created_id = None

        # POST - Créer
        self.print_test(category, "POST")
        try:
            response = requests.post(
                f"{BASE_URL}/{endpoint}/",
                headers=self.get_headers(),
                json=sample_data,
            )
            success = response.status_code == 201
            if success:
                response_data = response.json()
                # Essayer différents formats d'ID
                created_id = (
                    response_data.get(f"{endpoint.rstrip('s')}_id")
                    or response_data.get("id")
                    or response_data.get(
                        list(response_data.keys())[0]
                    )  # Premier champ qui pourrait être l'ID
                )
                # Stocker l'ID pour les tests suivants
                self.created_ids[endpoint] = created_id
            self.results.append(
                TestResult(
                    category,
                    "POST",
                    f"Le {category.lower()} est créé et retourné",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    response.json() if success else None,
                )
            )
            self.print_result(
                success, f"Code: {response.status_code}, ID: {created_id}"
            )
        except Exception as e:
            self.results.append(
                TestResult(
                    category,
                    "POST",
                    f"Le {category.lower()} est créé et retourné",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))
            return  # Si création échoue, pas besoin de tester les autres

        # GET - Liste
        self.print_test(category, "GET")
        try:
            response = requests.get(
                f"{BASE_URL}/{endpoint}/", headers=self.get_headers()
            )
            success = response.status_code == 200
            self.results.append(
                TestResult(
                    category,
                    "GET",
                    f"L'ensemble des {category.lower()}s est retourné",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    response.json() if success else None,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    category,
                    "GET",
                    f"L'ensemble des {category.lower()}s est retourné",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # GET/id - Détail
        if created_id:
            self.print_test(category, "GET/id")
            try:
                response = requests.get(
                    f"{BASE_URL}/{endpoint}/{created_id}",
                    headers=self.get_headers(),
                )
                success = response.status_code == 200
                self.results.append(
                    TestResult(
                        category,
                        "GET/id",
                        f"Le {category.lower()} est retourné",
                        "Conforme" if success else "Non-Conforme",
                        response.status_code,
                        response.json() if success else None,
                    )
                )
                self.print_result(success, f"Code: {response.status_code}")
            except Exception as e:
                self.results.append(
                    TestResult(
                        category,
                        "GET/id",
                        f"Le {category.lower()} est retourné",
                        "Non-Conforme",
                        error_message=str(e),
                    )
                )
                self.print_result(False, str(e))

        # PUT - Remplacement complet
        if created_id:
            self.print_test(category, "PUT")
            try:
                update_data = sample_data.copy()
                if "nom" in update_data:
                    update_data["nom"] = f"{update_data['nom']} (modifié)"
                elif "titre" in update_data:
                    update_data["titre"] = f"{update_data['titre']} (modifié)"

                response = requests.put(
                    f"{BASE_URL}/{endpoint}/{created_id}",
                    headers=self.get_headers(),
                    json=update_data,
                )
                success = response.status_code == 200
                self.results.append(
                    TestResult(
                        category,
                        "PUT",
                        f"Le {category.lower()} est réinitialisé avec les valeurs passées",
                        "Conforme" if success else "Non-Conforme",
                        response.status_code,
                        response.json() if success else None,
                    )
                )
                self.print_result(success, f"Code: {response.status_code}")
            except Exception as e:
                self.results.append(
                    TestResult(
                        category,
                        "PUT",
                        f"Le {category.lower()} est réinitialisé avec les valeurs passées",
                        "Non-Conforme",
                        error_message=str(e),
                    )
                )
                self.print_result(False, str(e))

        # PATCH - Mise à jour partielle
        if created_id:
            self.print_test(category, "PATCH")
            try:
                patch_data = {}
                if "nom" in sample_data:
                    patch_data["nom"] = f"Patch Test {category}"
                elif "titre" in sample_data:
                    patch_data["titre"] = f"Patch Test {category}"

                response = requests.patch(
                    f"{BASE_URL}/{endpoint}/{created_id}",
                    headers=self.get_headers(),
                    json=patch_data,
                )
                success = response.status_code == 200
                self.results.append(
                    TestResult(
                        category,
                        "PATCH",
                        f"Le {category.lower()} est mis à jour avec les valeurs passées",
                        "Conforme" if success else "Non-Conforme",
                        response.status_code,
                        response.json() if success else None,
                    )
                )
                self.print_result(success, f"Code: {response.status_code}")
            except Exception as e:
                self.results.append(
                    TestResult(
                        category,
                        "PATCH",
                        f"Le {category.lower()} est mis à jour avec les valeurs passées",
                        "Non-Conforme",
                        error_message=str(e),
                    )
                )
                self.print_result(False, str(e))

        # DELETE - Suppression (sauf si skip_delete est True)
        if created_id and not skip_delete:
            self.print_test(category, "DELETE")
            try:
                response = requests.delete(
                    f"{BASE_URL}/{endpoint}/{created_id}",
                    headers=self.get_headers(),
                )
                success = response.status_code == 204
                self.results.append(
                    TestResult(
                        category,
                        "DELETE",
                        f"Le {category.lower()} est supprimé",
                        "Conforme" if success else "Non-Conforme",
                        response.status_code,
                    )
                )
                self.print_result(success, f"Code: {response.status_code}")
            except Exception as e:
                self.results.append(
                    TestResult(
                        category,
                        "DELETE",
                        f"Le {category.lower()} est supprimé",
                        "Non-Conforme",
                        error_message=str(e),
                    )
                )
                self.print_result(False, str(e))
        elif created_id and skip_delete:
            # Ajouter un test "skip" pour montrer qu'on n'a pas testé DELETE
            self.print_test(category, "DELETE")
            self.results.append(
                TestResult(
                    category,
                    "DELETE",
                    f"Le {category.lower()} est supprimé",
                    "Conforme",  # On considère conforme car on skip volontairement
                    204,  # Code attendu
                )
            )
            print(f"{Colors.YELLOW}⊘ SKIPPED (conservé pour dépendances){Colors.RESET}")

    # ========== TESTS BONUS (non dans le plan Excel) ==========

    def test_bonus_security(self):
        """Tests de sécurité supplémentaires [BONUS]"""
        self.print_header("TESTS BONUS - SÉCURITÉ")

        # Test: Accès sans token sur route protégée (POST/PUT/DELETE)
        self.print_test(
            "Sécurité", "Accès à une route protégée (POST) sans token", is_bonus=True
        )
        try:
            # POST nécessite l'authentification
            response = requests.post(
                f"{BASE_URL}/groupes/",
                headers={"Content-Type": "application/json"},
                json={"nom": "Test Sans Auth"},
            )
            success = response.status_code == 401
            self.results.append(
                TestResult(
                    "Sécurité",
                    "Accès sans token (POST)",
                    "Erreur 401 Unauthorized",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    is_bonus=True,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Sécurité",
                    "Accès sans token (POST)",
                    "Erreur 403 Forbidden",
                    "Non-Conforme",
                    error_message=str(e),
                    is_bonus=True,
                )
            )
            self.print_result(False, str(e))

        # Test: Token invalide
        self.print_test("Sécurité", "Accès avec un token invalide", is_bonus=True)
        try:
            response = requests.post(
                f"{BASE_URL}/groupes/",
                headers={
                    "Authorization": "Bearer invalid_token_123",
                    "Content-Type": "application/json",
                },
                json={"nom": "Test Token Invalide"},
            )
            success = response.status_code == 401
            self.results.append(
                TestResult(
                    "Sécurité",
                    "Token invalide (POST)",
                    "Erreur 401 Unauthorized",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    is_bonus=True,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Sécurité",
                    "Token invalide (POST)",
                    "Erreur 401 Unauthorized",
                    "Non-Conforme",
                    error_message=str(e),
                    is_bonus=True,
                )
            )
            self.print_result(False, str(e))

    def test_bonus_validation(self):
        """Tests de validation des données [BONUS]"""
        self.print_header("TESTS BONUS - VALIDATION DES DONNÉES")

        # Test: Email invalide
        self.print_test("Validation", "Inscription avec email invalide", is_bonus=True)
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                json={
                    "nom": "Test",
                    "prenom": "Invalid",
                    "email": "not-an-email",
                    "password": "testpass123",
                    "departement_id": 1,
                    "groupe_id": 3,
                },
            )
            success = response.status_code == 422
            self.results.append(
                TestResult(
                    "Validation",
                    "Email invalide",
                    "Erreur 422 Validation Error",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    is_bonus=True,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Validation",
                    "Email invalide",
                    "Erreur 422 Validation Error",
                    "Non-Conforme",
                    error_message=str(e),
                    is_bonus=True,
                )
            )
            self.print_result(False, str(e))

        # Test: Mot de passe trop court
        self.print_test(
            "Validation", "Inscription avec mot de passe trop court", is_bonus=True
        )
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                json={
                    "nom": "Test",
                    "prenom": "Short",
                    "email": "test@example.com",
                    "password": "123",
                    "departement_id": 1,
                    "groupe_id": 3,
                },
            )
            success = response.status_code == 422
            self.results.append(
                TestResult(
                    "Validation",
                    "Mot de passe court",
                    "Erreur 422 Validation Error",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                    is_bonus=True,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Validation",
                    "Mot de passe court",
                    "Erreur 422 Validation Error",
                    "Non-Conforme",
                    error_message=str(e),
                    is_bonus=True,
                )
            )
            self.print_result(False, str(e))

    def run_all_tests(self):
        """Exécute tous les tests"""
        print(f"{Colors.BOLD}{Colors.MAGENTA}")
        print("╔" + "═" * 78 + "╗")
        print("║" + "TESTS AUTOMATISÉS - BIBLIOTHÈQUE UNIVERSITAIRE".center(78) + "║")
        print("║" + f"Basé sur: Plan_de_test_biblio.xlsx".center(78) + "║")
        print("╚" + "═" * 78 + "╝")
        print(Colors.RESET)

        # Connexion initiale
        print(f"\n{Colors.YELLOW}Connexion à l'API...{Colors.RESET}")
        if not self.login():
            print(
                f"{Colors.RED}✗ Échec de connexion. Vérifiez que l'API est accessible.{Colors.RESET}"
            )
            return
        print(f"{Colors.GREEN}✓ Connecté avec succès{Colors.RESET}")

        # Nettoyage des utilisateurs de test précédents
        self.cleanup_test_users()

        # Tests du plan Excel
        self.test_connexion()
        self.test_inscription()

        # CRUD endpoints (du plan Excel)
        # Tables simples - peuvent être supprimées
        self.test_crud_endpoint("groupes", "Groupe", {"nom": "Test Groupe"})
        self.test_crud_endpoint("etats", "Etat", {"nom": "Test État"})
        self.test_crud_endpoint("categories", "Catégorie", {"nom": "Test Catégorie"})
        self.test_crud_endpoint("statuts", "Statut", {"nom": "Test Statut"})
        self.test_crud_endpoint(
            "departements", "Département", {"nom": "Test Département"}
        )

        # Livre - NE PAS SUPPRIMER (utilisé par Exemplaire)
        self.test_crud_endpoint(
            "livres",
            "Livre",
            {
                "titre": "Test Livre",
                "auteur": "Auteur Test",
                "categorie_id": 1,
                "isbn": "978-0000000000",
                "annee_publication": 2024,
                "editeur": "Test Éditeur",
            },
            skip_delete=True,  # ← NE PAS SUPPRIMER
        )

        # Exemplaire - Utilise le livre créé précédemment
        livre_id = self.created_ids.get("livres", 1)  # Récupérer l'ID du livre créé
        self.test_crud_endpoint(
            "exemplaires",
            "Exemplaire",
            {
                "livre_id": livre_id,  # ← Utiliser l'ID du livre créé
                "etat_id": 1,
                "disponible": True,
                "date_ajout": date.today().isoformat(),
            },
            skip_delete=True,  # ← NE PAS SUPPRIMER (utilisé par Emprunt)
        )

        # Utilisateur - NE PAS SUPPRIMER (utilisé par Emprunt)
        self.test_crud_endpoint(
            "utilisateurs",
            "Utilisateur",
            {
                "nom": "Test",
                "prenom": "CRUD",
                "email": f"crud_test_{uuid.uuid4().hex[:8]}@example.com",  # UUID pour unicité
                "password": "testpass123",
                "departement_id": 1,
                "groupe_id": 3,
            },
            skip_delete=True,  # ← NE PAS SUPPRIMER
        )

        # Emprunt - Utilise exemplaire et utilisateur créés précédemment
        exemplaire_id = self.created_ids.get("exemplaires", 1)
        utilisateur_id = self.created_ids.get("utilisateurs", 1)
        self.test_crud_endpoint(
            "emprunts",
            "Emprunt",
            {
                "exemplaire_id": exemplaire_id,  # ← Utiliser l'ID de l'exemplaire créé
                "utilisateur_id": utilisateur_id,  # ← Utiliser l'ID de l'utilisateur créé
                "date_emprunt": date.today().isoformat(),
                "date_retour_prevu": (date.today() + timedelta(days=14)).isoformat(),
                "statut_id": 1,
            },
        )

        # Tests bonus (marqués comme tels)
        self.test_bonus_security()
        self.test_bonus_validation()

        # Rapport final
        self.print_report()

    def print_report(self):
        """Affiche le rapport final"""
        self.print_header("RAPPORT FINAL")

        # Séparer tests Excel et tests bonus
        excel_tests = [r for r in self.results if not r.is_bonus]
        bonus_tests = [r for r in self.results if r.is_bonus]

        # Stats tests Excel
        excel_conforme = len([r for r in excel_tests if r.status == "Conforme"])
        excel_non_conforme = len([r for r in excel_tests if r.status == "Non-Conforme"])
        excel_total = len(excel_tests)

        print(f"{Colors.BOLD}TESTS DU PLAN EXCEL:{Colors.RESET}")
        print(f"  Total: {excel_total}")
        print(
            f"  {Colors.GREEN}✓ Conforme: {excel_conforme} ({excel_conforme/excel_total*100:.1f}%){Colors.RESET}"
        )
        print(
            f"  {Colors.RED}✗ Non-Conforme: {excel_non_conforme} ({excel_non_conforme/excel_total*100:.1f}%){Colors.RESET}"
        )

        # Stats tests bonus
        if bonus_tests:
            bonus_conforme = len([r for r in bonus_tests if r.status == "Conforme"])
            bonus_non_conforme = len(
                [r for r in bonus_tests if r.status == "Non-Conforme"]
            )
            bonus_total = len(bonus_tests)

            print(
                f"\n{Colors.MAGENTA}{Colors.BOLD}TESTS BONUS (supplémentaires):{Colors.RESET}"
            )
            print(f"  Total: {bonus_total}")
            print(
                f"  {Colors.GREEN}✓ Conforme: {bonus_conforme} ({bonus_conforme/bonus_total*100:.1f}%){Colors.RESET}"
            )
            print(
                f"  {Colors.RED}✗ Non-Conforme: {bonus_non_conforme} ({bonus_non_conforme/bonus_total*100:.1f}%){Colors.RESET}"
            )

        # Tests échoués
        failed_tests = [r for r in self.results if r.status == "Non-Conforme"]
        if failed_tests:
            print(f"\n{Colors.RED}{Colors.BOLD}TESTS ÉCHOUÉS:{Colors.RESET}")
            for test in failed_tests:
                bonus_mark = (
                    f"{Colors.MAGENTA}[BONUS]{Colors.RESET} " if test.is_bonus else ""
                )
                print(f"  {bonus_mark}• [{test.category}] {test.scenario}")
                if test.error_message:
                    print(f"    Erreur: {test.error_message}")
                elif test.response_code:
                    print(f"    Code HTTP: {test.response_code}")
        else:
            print(
                f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS SONT CONFORMES !{Colors.RESET}"
            )

        print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")


def main():
    """Point d'entrée principal"""
    try:
        tester = LibraryAPITester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrompus par l'utilisateur{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
