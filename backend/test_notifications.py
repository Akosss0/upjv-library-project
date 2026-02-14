#!/usr/bin/env python3
"""
Script de test automatisé pour le système de NOTIFICATIONS
Tests des rappels J-30, J-5 et des retards avec différents rôles utilisateurs

Ce script :
1. Crée des emprunts de test avec différentes dates
2. Teste les permissions par rôle (Bibliothécaire, Professeur, Élève)
3. Vérifie que les notifications sont correctes
4. Nettoie automatiquement toutes les données de test à la fin
"""

import requests
import json
from datetime import date, timedelta
from typing import Dict, Any, List
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
    status: str
    response_code: int = None
    response_data: Any = None
    error_message: str = None


class NotificationsTester:
    def __init__(self):
        self.token = None
        self.results: List[TestResult] = []
        self.created_data = {
            "users": [],
            "livres": [],
            "exemplaires": [],
            "emprunts": [],
        }
        self.test_users = {}

    def print_header(self, text: str):
        """Affiche un header coloré"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")

    def print_test(self, category: str, scenario: str):
        """Affiche le test en cours"""
        print(f"{Colors.BLUE}[{category}]{Colors.RESET} {scenario}...", end=" ")

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

    def login(self, email: str = ADMIN_EMAIL, password: str = ADMIN_PASSWORD) -> str:
        """Connexion et récupération du token"""
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"email": email, "password": password},
            )
            if response.status_code == 200:
                return response.json()["access_token"]
            return None
        except Exception as e:
            print(f"{Colors.RED}Erreur de connexion: {e}{Colors.RESET}")
            return None

    def get_headers(self, token: str = None) -> Dict[str, str]:
        """Retourne les headers avec le token"""
        if token is None:
            token = self.token
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    # ========== SETUP: Création des données de test ==========

    def setup_test_data(self):
        """Crée toutes les données de test nécessaires"""
        self.print_header("PRÉPARATION DES DONNÉES DE TEST")

        print(f"{Colors.YELLOW}Création des utilisateurs de test...{Colors.RESET}")

        # Créer 3 utilisateurs (un par groupe)
        try:
            # Bibliothécaire
            biblio = self.create_user("Bibliothecaire", 1)
            self.test_users["bibliothecaire"] = biblio
            self.created_data["users"].append(biblio["user_id"])

            # Professeur
            prof = self.create_user("Professeur", 2)
            self.test_users["professeur"] = prof
            self.created_data["users"].append(prof["user_id"])

            # Élève
            eleve = self.create_user("Eleve", 3)
            self.test_users["eleve"] = eleve
            self.created_data["users"].append(eleve["user_id"])

            print(f"{Colors.GREEN}✓ 3 utilisateurs créés{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✗ Erreur création utilisateurs: {e}{Colors.RESET}")
            return False

        print(f"{Colors.YELLOW}Création des livres et exemplaires...{Colors.RESET}")

        # Créer 4 livres
        try:
            for i in range(4):
                livre_id = self.create_livre(f"Livre Test Notif {i+1}")
                self.created_data["livres"].append(livre_id)

                exemplaire_id = self.create_exemplaire(livre_id)
                self.created_data["exemplaires"].append(exemplaire_id)

            print(f"{Colors.GREEN}✓ 4 livres et exemplaires créés{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}✗ Erreur création livres: {e}{Colors.RESET}")
            return False

        print(f"{Colors.YELLOW}Création des emprunts de test...{Colors.RESET}")

        # Créer des emprunts avec différentes dates
        try:
            today = date.today()

            # Emprunt 1: EN RETARD (15 jours)
            emprunt1 = self.create_emprunt(
                self.created_data["exemplaires"][0],
                self.test_users["eleve"]["user_id"],
                today - timedelta(days=45),  # Emprunté il y a 45 jours
                today - timedelta(days=15),  # Devait être rendu il y a 15 jours
            )
            self.created_data["emprunts"].append(emprunt1)

            # Emprunt 2: EN RETARD (5 jours)
            emprunt2 = self.create_emprunt(
                self.created_data["exemplaires"][1],
                self.test_users["professeur"]["user_id"],
                today - timedelta(days=35),
                today - timedelta(days=5),
            )
            self.created_data["emprunts"].append(emprunt2)

            # Emprunt 3: RAPPEL J-30
            emprunt3 = self.create_emprunt(
                self.created_data["exemplaires"][2],
                self.test_users["eleve"]["user_id"],
                today,
                today + timedelta(days=30),  # À rendre dans exactement 30 jours
            )
            self.created_data["emprunts"].append(emprunt3)

            # Emprunt 4: RAPPEL J-5
            emprunt4 = self.create_emprunt(
                self.created_data["exemplaires"][3],
                self.test_users["professeur"]["user_id"],
                today - timedelta(days=9),
                today + timedelta(days=5),  # À rendre dans exactement 5 jours
            )
            self.created_data["emprunts"].append(emprunt4)

            print(f"{Colors.GREEN}✓ 4 emprunts créés:{Colors.RESET}")
            print(f"  • 2 en retard (15j et 5j)")
            print(f"  • 1 rappel J-30")
            print(f"  • 1 rappel J-5")

        except Exception as e:
            print(f"{Colors.RED}✗ Erreur création emprunts: {e}{Colors.RESET}")
            return False

        return True

    def create_user(self, groupe_name: str, groupe_id: int) -> Dict[str, Any]:
        """Crée un utilisateur de test"""
        email = f"notif_test_{groupe_name.lower()}_{uuid.uuid4().hex[:8]}@example.com"
        password = "testpass123"

        response = requests.post(
            f"{BASE_URL}/register",
            json={
                "nom": f"Test",
                "prenom": groupe_name,
                "email": email,
                "password": password,
                "departement_id": 1,
                "groupe_id": groupe_id,
            },
        )

        if response.status_code != 201:
            raise Exception(f"Création utilisateur échouée: {response.status_code}")

        user_data = response.json()
        token = self.login(email, password)

        return {
            "email": email,
            "password": password,
            "token": token,
            "user_id": user_data.get("utilisateurs_id"),
            "groupe": groupe_name,
        }

    def create_livre(self, titre: str) -> int:
        """Crée un livre de test"""
        response = requests.post(
            f"{BASE_URL}/livres/",
            headers=self.get_headers(),
            json={
                "titre": titre,
                "auteur": "Auteur Test",
                "categorie_id": 1,
                "isbn": f"978-{uuid.uuid4().hex[:10]}",
                "annee_publication": 2024,
                "editeur": "Test Publisher",
            },
        )

        if response.status_code != 201:
            raise Exception(f"Création livre échouée: {response.status_code}")

        return response.json()["livre_id"]

    def create_exemplaire(self, livre_id: int) -> int:
        """Crée un exemplaire de test"""
        response = requests.post(
            f"{BASE_URL}/exemplaires/",
            headers=self.get_headers(),
            json={
                "livre_id": livre_id,
                "etat_id": 1,
                "disponible": False,  # Déjà emprunté
                "date_ajout": date.today().isoformat(),
            },
        )

        if response.status_code != 201:
            raise Exception(f"Création exemplaire échouée: {response.status_code}")

        return response.json()["exemplaire_id"]

    def create_emprunt(
        self,
        exemplaire_id: int,
        user_id: int,
        date_emprunt: date,
        date_retour_prevu: date,
    ) -> int:
        """Crée un emprunt de test avec des dates spécifiques"""
        response = requests.post(
            f"{BASE_URL}/emprunts/",
            headers=self.get_headers(),
            json={
                "exemplaire_id": exemplaire_id,
                "utilisateur_id": user_id,
                "date_emprunt": date_emprunt.isoformat(),
                "date_retour_prevu": date_retour_prevu.isoformat(),
                "statut_id": 1,
            },
        )

        if response.status_code != 201:
            raise Exception(f"Création emprunt échouée: {response.status_code}")

        return response.json()["emprunt_id"]

    # ========== TESTS: Permissions par rôle ==========

    def test_permissions_bibliothecaire(self):
        """Tests d'accès pour un bibliothécaire"""
        self.print_header("TESTS PERMISSIONS - BIBLIOTHÉCAIRE")

        token = self.test_users["bibliothecaire"]["token"]

        # Test 1: Accès à /notifications/retards
        self.print_test("Bibliothécaire", "GET /notifications/retards (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/retards", headers=self.get_headers(token)
            )
            success = response.status_code == 200
            data = response.json() if success else None

            # Vérifier qu'on a bien 2 retards
            if success and len(data) == 2:
                extra_success = True
                details = f"Code: {response.status_code}, {len(data)} retards trouvés ✓"
            else:
                extra_success = False
                details = f"Code: {response.status_code}, attendu 2 retards, reçu {len(data) if data else 0}"

            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /retards",
                    "200 OK avec 2 retards",
                    "Conforme" if (success and extra_success) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and extra_success, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /retards",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 2: Accès à /notifications/rappels/j30
        self.print_test("Bibliothécaire", "GET /notifications/rappels/j30 (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/rappels/j30", headers=self.get_headers(token)
            )
            success = response.status_code == 200
            data = response.json() if success else None

            if success and len(data) == 1:
                extra_success = True
                details = f"Code: {response.status_code}, 1 rappel J-30 trouvé ✓"
            else:
                extra_success = False
                details = f"Code: {response.status_code}, attendu 1 rappel, reçu {len(data) if data else 0}"

            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /rappels/j30",
                    "200 OK avec 1 rappel",
                    "Conforme" if (success and extra_success) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and extra_success, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /rappels/j30",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 3: Accès à /notifications/rappels/j5
        self.print_test("Bibliothécaire", "GET /notifications/rappels/j5 (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/rappels/j5", headers=self.get_headers(token)
            )
            success = response.status_code == 200
            data = response.json() if success else None

            if success and len(data) == 1:
                extra_success = True
                details = f"Code: {response.status_code}, 1 rappel J-5 trouvé ✓"
            else:
                extra_success = False
                details = f"Code: {response.status_code}, attendu 1 rappel, reçu {len(data) if data else 0}"

            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /rappels/j5",
                    "200 OK avec 1 rappel",
                    "Conforme" if (success and extra_success) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and extra_success, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /rappels/j5",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 4: Accès à /notifications/tous
        self.print_test("Bibliothécaire", "GET /notifications/tous (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/tous", headers=self.get_headers(token)
            )
            success = response.status_code == 200
            data = response.json() if success else None

            if success and data:
                checks = (
                    len(data.get("en_retard", [])) == 2
                    and len(data.get("rappel_j30", [])) == 1
                    and len(data.get("rappel_j5", [])) == 1
                )
                details = f"Code: {response.status_code}, 2 retards, 1 J-30, 1 J-5 ✓"
            else:
                checks = False
                details = f"Code: {response.status_code}, données incorrectes"

            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /tous",
                    "200 OK avec toutes les notifs",
                    "Conforme" if (success and checks) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and checks, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Biblio",
                    "GET /tous",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

    def test_permissions_professeur(self):
        """Tests d'accès pour un professeur (doit être refusé)"""
        self.print_header("TESTS PERMISSIONS - PROFESSEUR (REFUS ATTENDU)")

        token = self.test_users["professeur"]["token"]

        # Test 1: Refus /notifications/retards
        self.print_test("Professeur", "GET /notifications/retards (refusé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/retards", headers=self.get_headers(token)
            )
            success = response.status_code == 403

            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /retards (refus)",
                    "403 Forbidden",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /retards (refus)",
                    "403 Forbidden",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 2: Refus /notifications/rappels/j30
        self.print_test("Professeur", "GET /notifications/rappels/j30 (refusé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/rappels/j30", headers=self.get_headers(token)
            )
            success = response.status_code == 403

            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /rappels/j30 (refus)",
                    "403 Forbidden",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /rappels/j30 (refus)",
                    "403 Forbidden",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 3: Accès autorisé à /notifications/mes-notifications
        self.print_test("Professeur", "GET /mes-notifications (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/mes-notifications",
                headers=self.get_headers(token),
            )
            success = response.status_code == 200
            data = response.json() if success else None

            # Le professeur a 1 retard et 1 rappel J-5
            if success and data:
                checks = (
                    len(data.get("en_retard", [])) == 1
                    and len(data.get("rappel_j5", [])) == 1
                )
                details = f"Code: {response.status_code}, 1 retard, 1 J-5 ✓"
            else:
                checks = False
                details = f"Code: {response.status_code}"

            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /mes-notifications",
                    "200 OK",
                    "Conforme" if (success and checks) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and checks, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Prof",
                    "GET /mes-notifications",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

    def test_permissions_eleve(self):
        """Tests d'accès pour un élève"""
        self.print_header("TESTS PERMISSIONS - ÉLÈVE")

        token = self.test_users["eleve"]["token"]

        # Test 1: Refus /notifications/retards
        self.print_test("Élève", "GET /notifications/retards (refusé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/retards", headers=self.get_headers(token)
            )
            success = response.status_code == 403

            self.results.append(
                TestResult(
                    "Permissions Élève",
                    "GET /retards (refus)",
                    "403 Forbidden",
                    "Conforme" if success else "Non-Conforme",
                    response.status_code,
                )
            )
            self.print_result(success, f"Code: {response.status_code}")
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Élève",
                    "GET /retards (refus)",
                    "403 Forbidden",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

        # Test 2: Accès autorisé à /notifications/mes-notifications
        self.print_test("Élève", "GET /mes-notifications (autorisé)")
        try:
            response = requests.get(
                f"{BASE_URL}/notifications/mes-notifications",
                headers=self.get_headers(token),
            )
            success = response.status_code == 200
            data = response.json() if success else None

            # L'élève a 1 retard et 1 rappel J-30
            if success and data:
                checks = (
                    len(data.get("en_retard", [])) == 1
                    and len(data.get("rappel_j30", [])) == 1
                )
                details = f"Code: {response.status_code}, 1 retard, 1 J-30 ✓"
            else:
                checks = False
                details = f"Code: {response.status_code}"

            self.results.append(
                TestResult(
                    "Permissions Élève",
                    "GET /mes-notifications",
                    "200 OK",
                    "Conforme" if (success and checks) else "Non-Conforme",
                    response.status_code,
                    data,
                )
            )
            self.print_result(success and checks, details)
        except Exception as e:
            self.results.append(
                TestResult(
                    "Permissions Élève",
                    "GET /mes-notifications",
                    "200 OK",
                    "Non-Conforme",
                    error_message=str(e),
                )
            )
            self.print_result(False, str(e))

    # ========== CLEANUP: Suppression des données de test ==========

    def cleanup_test_data(self):
        """Supprime toutes les données de test créées"""
        self.print_header("NETTOYAGE DES DONNÉES DE TEST")

        print(f"{Colors.YELLOW}Suppression des données créées...{Colors.RESET}")

        deleted = {"emprunts": 0, "exemplaires": 0, "livres": 0, "users": 0}

        # Supprimer les emprunts
        for emprunt_id in self.created_data["emprunts"]:
            try:
                response = requests.delete(
                    f"{BASE_URL}/emprunts/{emprunt_id}", headers=self.get_headers()
                )
                if response.status_code == 204:
                    deleted["emprunts"] += 1
            except:
                pass

        # Supprimer les exemplaires
        for exemplaire_id in self.created_data["exemplaires"]:
            try:
                response = requests.delete(
                    f"{BASE_URL}/exemplaires/{exemplaire_id}",
                    headers=self.get_headers(),
                )
                if response.status_code == 204:
                    deleted["exemplaires"] += 1
            except:
                pass

        # Supprimer les livres
        for livre_id in self.created_data["livres"]:
            try:
                response = requests.delete(
                    f"{BASE_URL}/livres/{livre_id}", headers=self.get_headers()
                )
                if response.status_code == 204:
                    deleted["livres"] += 1
            except:
                pass

        # Supprimer les utilisateurs
        for user_id in self.created_data["users"]:
            try:
                response = requests.delete(
                    f"{BASE_URL}/utilisateurs/{user_id}", headers=self.get_headers()
                )
                if response.status_code == 204:
                    deleted["users"] += 1
            except:
                pass

        print(f"{Colors.GREEN}✓ Nettoyage terminé:{Colors.RESET}")
        print(
            f"  • {deleted['emprunts']}/{len(self.created_data['emprunts'])} emprunts supprimés"
        )
        print(
            f"  • {deleted['exemplaires']}/{len(self.created_data['exemplaires'])} exemplaires supprimés"
        )
        print(
            f"  • {deleted['livres']}/{len(self.created_data['livres'])} livres supprimés"
        )
        print(
            f"  • {deleted['users']}/{len(self.created_data['users'])} utilisateurs supprimés"
        )

    # ========== RAPPORT ==========

    def print_report(self):
        """Affiche le rapport final"""
        self.print_header("RAPPORT FINAL DES TESTS NOTIFICATIONS")

        conforme = len([r for r in self.results if r.status == "Conforme"])
        non_conforme = len([r for r in self.results if r.status == "Non-Conforme"])
        total = len(self.results)

        print(f"{Colors.BOLD}RÉSULTATS:{Colors.RESET}")
        print(f"  Total: {total} tests")
        print(
            f"  {Colors.GREEN}✓ Conforme: {conforme} ({conforme/total*100:.1f}%){Colors.RESET}"
        )
        print(
            f"  {Colors.RED}✗ Non-Conforme: {non_conforme} ({non_conforme/total*100:.1f}%){Colors.RESET}"
        )

        # Tests échoués
        failed_tests = [r for r in self.results if r.status == "Non-Conforme"]
        if failed_tests:
            print(f"\n{Colors.RED}{Colors.BOLD}TESTS ÉCHOUÉS:{Colors.RESET}")
            for test in failed_tests:
                print(f"  • [{test.category}] {test.scenario}")
                if test.error_message:
                    print(f"    Erreur: {test.error_message}")
                elif test.response_code:
                    print(f"    Code HTTP: {test.response_code}")
        else:
            print(
                f"\n{Colors.GREEN}{Colors.BOLD}🎉 TOUS LES TESTS SONT CONFORMES !{Colors.RESET}"
            )

        print(f"\n{Colors.CYAN}{'='*80}{Colors.RESET}")

    # ========== MAIN ==========

    def run_all_tests(self):
        """Exécute tous les tests"""
        print(f"{Colors.BOLD}{Colors.MAGENTA}")
        print("╔" + "═" * 78 + "╗")
        print("║" + "TESTS AUTOMATISÉS - SYSTÈME DE NOTIFICATIONS".center(78) + "║")
        print(
            "║" + "Rappels J-30, J-5 et Retards par rôle utilisateur".center(78) + "║"
        )
        print("╚" + "═" * 78 + "╝")
        print(Colors.RESET)

        # Connexion admin
        print(f"\n{Colors.YELLOW}Connexion en tant qu'administrateur...{Colors.RESET}")
        self.token = self.login()
        if not self.token:
            print(f"{Colors.RED}✗ Échec de connexion{Colors.RESET}")
            return
        print(f"{Colors.GREEN}✓ Connecté{Colors.RESET}")

        # Setup
        if not self.setup_test_data():
            print(f"{Colors.RED}✗ Échec de la préparation des données{Colors.RESET}")
            return

        # Tests
        self.test_permissions_bibliothecaire()
        self.test_permissions_professeur()
        self.test_permissions_eleve()

        # Cleanup
        self.cleanup_test_data()

        # Rapport
        self.print_report()


def main():
    """Point d'entrée principal"""
    try:
        tester = NotificationsTester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrompus par l'utilisateur{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
