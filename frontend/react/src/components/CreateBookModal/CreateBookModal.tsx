import React, { useState } from 'react';
import './CreateBookModal.css';
import { BookService } from '../BookLine/Book.service';
import { type BookProps } from '../BookLine/BookLine';

interface CreateBookModalProps {
    isOpen: boolean;
    onClose: () => void;
    onBookCreated?: () => void; // Callback pour rafraîchir la liste
}

export function CreateBookModal({ isOpen, onClose, onBookCreated }: CreateBookModalProps) {
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // État du formulaire
    const [formData, setFormData] = useState<Omit<BookProps, "livre_id">>({
        titre: '',
        auteur: '',
        isbn: '',
        annee_publication: new Date().getFullYear(),
        resume: ''
    });

    if (!isOpen) return null;

    const stopPropagation = (e: React.MouseEvent) => e.stopPropagation();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [id]: id === 'year' ? parseInt(value) || 0 : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setError(null);

        try {
            // Validation basique
            if (!formData.titre || !formData.auteur) {
                setError("Le titre et l'auteur sont obligatoires");
                setIsSubmitting(false);
                return;
            }

            // Appel à l'API
            const newBook = await BookService.postBook(formData);

            if (newBook) {
                // Succès
                console.log("Livre créé avec succès:", newBook);

                // Réinitialiser le formulaire
                setFormData({
                    titre: '',
                    auteur: '',
                    isbn: '',
                    annee_publication: new Date().getFullYear(),
                    resume: '',
                });

                // Callback pour rafraîchir la liste
                onBookCreated?.();

                // Fermer la modale
                onClose();
            } else {
                setError("Erreur lors de la création du livre");
            }
        } catch (err) {
            console.error("Erreur:", err);
            setError("Une erreur s'est produite");
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleClose = () => {
        // Réinitialiser l'erreur et fermer
        setError(null);
        onClose();
    };

    return (
        <div className="modal-overlay" onClick={handleClose}>
            <div className="modal-container" onClick={stopPropagation}>
                <header className="modal-header">
                    <h2>Ajouter un nouvel ouvrage</h2>
                    <button
                        className="close-button"
                        onClick={handleClose}
                        aria-label="Fermer"
                        disabled={isSubmitting}
                    >
                        &times;
                    </button>
                </header>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <form className="modal-form" onSubmit={handleSubmit}>
                    <div className="form-grid">
                        <div className="input-group">
                            <label htmlFor="title">Titre du livre *</label>
                            <input
                                type="text"
                                id="titre"
                                placeholder="Ex: Michel Strogoff"
                                value={formData.titre}
                                onChange={handleChange}
                                required
                                disabled={isSubmitting}
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="author">Auteur *</label>
                            <input
                                type="text"
                                id="auteur"
                                placeholder="Ex: Jules Verne"
                                value={formData.auteur}
                                onChange={handleChange}
                                required
                                disabled={isSubmitting}
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="isbn">ISBN</label>
                            <input
                                type="text"
                                id="isbn"
                                placeholder="978-2070409102"
                                value={formData.isbn}
                                onChange={handleChange}
                                disabled={isSubmitting}
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="status">Statut initial</label>
                            <select
                                onChange={handleChange}
                                disabled={isSubmitting}
                            >
                                <option value="available">Disponible</option>
                                <option value="borrowed">Emprunté</option>
                                <option value="reserved">Réservé</option>
                                <option value="unavailable">Indisponible</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label htmlFor="year">Année de parution</label>
                            <input
                                type="number"
                                id="annee_publication"
                                placeholder="1876"
                                value={formData.annee_publication}
                                onChange={handleChange}
                                min="1000"
                                max={new Date().getFullYear() + 1}
                                disabled={isSubmitting}
                            />
                        </div>

                        <div className="input-group">
                            <label htmlFor="cover">URL de la couverture</label>
                            <input
                                type="url"
                                value="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHOpD8bvVfGOjLGwVMyUwlk_c-y-GpufiWJw&s"
                                placeholder="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHOpD8bvVfGOjLGwVMyUwlk_c-y-GpufiWJw&s"
                                onChange={handleChange}
                                disabled={isSubmitting}
                            />
                        </div>
                    </div>

                    <div className="input-group full-width">
                        <label htmlFor="description">Résumé</label>
                        <textarea
                            id="resume"
                            rows={3}
                            placeholder="Description de l'œuvre..."
                            value={formData.resume}
                            onChange={handleChange}
                            disabled={isSubmitting}
                        ></textarea>
                    </div>

                    <footer className="modal-actions">
                        <button
                            type="button"
                            className="btn-secondary"
                            onClick={handleClose}
                            disabled={isSubmitting}
                        >
                            Annuler
                        </button>
                        <button
                            type="submit"
                            className="btn-primary"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Enregistrement...' : 'Enregistrer le livre'}
                        </button>
                    </footer>
                </form>
            </div>
        </div>
    );
}