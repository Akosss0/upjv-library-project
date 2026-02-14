import React from 'react';
import './CreateBookModal.css';

interface CreateBookModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function CreateBookModal({ isOpen, onClose }: CreateBookModalProps) {
    if (!isOpen) return null;

    const stopPropagation = (e: React.MouseEvent) => e.stopPropagation();

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-container" onClick={stopPropagation}>
                <header className="modal-header">
                    <h2>Ajouter un nouvel ouvrage</h2>
                    <button className="close-button" onClick={onClose} aria-label="Fermer">
                        &times;
                    </button>
                </header>

                <form className="modal-form" onSubmit={(e) => e.preventDefault()}>
                    <div className="form-grid">
                        <div className="input-group">
                            <label htmlFor="title">Titre du livre</label>
                            <input type="text" id="title" placeholder="Ex: Michel Strogoff" required />
                        </div>

                        <div className="input-group">
                            <label htmlFor="author">Auteur</label>
                            <input type="text" id="author" placeholder="Ex: Jules Verne" required />
                        </div>

                        {/* Nouveaux champs : ISBN et Status */}
                        <div className="input-group">
                            <label htmlFor="isbn">ISBN</label>
                            <input type="text" id="isbn" placeholder="978-2070409102" required />
                        </div>

                        <div className="input-group">
                            <label htmlFor="status">Statut initial</label>
                            <select id="status" defaultValue="available">
                                <option value="available">Disponible</option>
                                <option value="borrowed">Emprunté</option>
                                <option value="maintenance">En réparation</option>
                                <option value="reserved">Réservé</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label htmlFor="genre">Genre</label>
                            <select id="genre">
                                <option value="aventure">Aventure</option>
                                <option value="roman">Roman</option>
                                <option value="science-fiction">Science-Fiction</option>
                                <option value="histoire">Histoire</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label htmlFor="year">Année de parution</label>
                            <input type="number" id="year" placeholder="1876" />
                        </div>
                    </div>

                    <div className="input-group full-width">
                        <label htmlFor="resume">Résumé</label>
                        <textarea id="resume" rows={3} placeholder="Description de l'œuvre..."></textarea>
                    </div>

                    <footer className="modal-actions">
                        <button type="button" className="btn-secondary" onClick={onClose}>Annuler</button>
                        <button type="submit" className="btn-primary">Enregistrer le livre</button>
                    </footer>
                </form>
            </div>
        </div>
    );
}