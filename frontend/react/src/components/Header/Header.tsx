import "./Header.css";
import backgroundImage from "../../assets/librairy.png";
import headerImage from "../../assets/verne_sign.png";
import { CreateBookModal } from "../CreateBookModal/CreateBookModal";
import { useState } from "react";

// Ajout de la prop isAdmin (par défaut false)
export function Header({ isAdmin = true }) {
    const [showModal, setShowModal] = useState(false);

    return (
        <header className="hero-header">
            <nav className="top-nav" aria-label="Navigation principale">
                <a href="/" className="logo-link">
                    <img src={headerImage} className="logo" alt="Jules Verne - Accueil" />
                </a>

                <div className="nav-links">
                    <a className="nav-item" href="/emprunts">Mes emprunts</a>
                    <a className="nav-item" href="/stats">Statistiques</a>
                    <a className="user-avatar" href="/profil" aria-label="Mon profil">
                        <img src="/logo.png" alt="Avatar utilisateur" />
                    </a>
                </div>
            </nav>

            <div className="hero-content">
                <div className="search-container">
                    <form className="search-form" role="search">
                        <div className="search-group">
                            <input type="text" placeholder="Les Fleurs du Mal..." aria-label="Rechercher un livre" />
                            <button type="submit" className="search-button">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                                    <path fillRule="evenodd" d="M10.5 3.75a6.75 6.75 0 1 0 0 13.5 6.75 6.75 0 0 0 0-13.5ZM2.25 10.5a8.25 8.25 0 1 1 14.59 5.28l4.69 4.69a.75.75 0 1 1-1.06 1.06l-4.69-4.69A8.25 8.25 0 0 1 2.25 10.5Z" clipRule="evenodd" />
                                </svg>
                                <span>Rechercher</span>
                            </button>
                        </div>
                    </form>

                    {/* Affichage conditionnel des boutons Admin */}
                    {isAdmin && (
                        <div className="admin-actions">
                            <button onClick={() => setShowModal(true)} className="admin-btn">Ajouter un livre</button>
                        </div>
                    )}
                </div>
            </div>

            <div className="hero-background">
                <img src={backgroundImage} alt="" aria-hidden="true" />
            </div>
            <CreateBookModal isOpen={showModal} onClose={() => setShowModal(false)} />
        </header>

    );
}