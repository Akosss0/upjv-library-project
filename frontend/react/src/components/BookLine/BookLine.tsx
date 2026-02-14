import "./BookLine.css";
import { isAdmin } from "../../App";

export type BookProps = {
    livre_id: number,
    titre: string,
    auteur: string,
    resume: string,
    annee_publication: number,
    isbn: string,
};

interface BookLineProps {
    book: BookProps;
}

const status = "emprunté";

export function BookLine({ book }: BookLineProps) {

    // Fonction pour obtenir les boutons en fonction du statut et du rôle
    const getActionButtons = (status: string) => {
        if (isAdmin) {
            // Admin voit toujours Modifier et Supprimer

            switch (status) {
                case "available":
                case "disponible":
                    return (
                        <>
                            <button className="loan-button edit-button" aria-label="Modifier ce livre">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                                    <path d="M21.731 2.269a2.625 2.625 0 0 0-3.712 0l-1.157 1.157 3.712 3.712 1.157-1.157a2.625 2.625 0 0 0 0-3.712ZM19.513 8.199l-3.712-3.712-8.4 8.4a5.25 5.25 0 0 0-1.32 2.214l-.8 2.685a.75.75 0 0 0 .933.933l2.685-.8a5.25 5.25 0 0 0 2.214-1.32l8.4-8.4Z" />
                                    <path d="M5.25 5.25a3 3 0 0 0-3 3v10.5a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3V13.5a.75.75 0 0 0-1.5 0v5.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5V8.25a1.5 1.5 0 0 1 1.5-1.5h5.25a.75.75 0 0 0 0-1.5H5.25Z" />
                                </svg>
                                <span className="loan-text">Modifier</span>
                            </button>
                            <button className="loan-button delete-button" aria-label="Supprimer ce livre">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                                    <path d="M3.375 3C2.339 3 1.5 3.84 1.5 4.875v.75c0 1.036.84 1.875 1.875 1.875h17.25c1.035 0 1.875-.84 1.875-1.875v-.75C22.5 3.839 21.66 3 20.625 3H3.375Z" />
                                    <path fillRule="evenodd" d="m3.087 9 .54 9.176A3 3 0 0 0 6.62 21h10.757a3 3 0 0 0 2.995-2.824L20.913 9H3.087Zm6.133 2.845a.75.75 0 0 1 1.06 0l1.72 1.72 1.72-1.72a.75.75 0 1 1 1.06 1.06l-1.72 1.72 1.72 1.72a.75.75 0 1 1-1.06 1.06L12 15.685l-1.72 1.72a.75.75 0 1 1-1.06-1.06l1.72-1.72-1.72-1.72a.75.75 0 0 1 0-1.06Z" clipRule="evenodd" />
                                </svg>
                                <span className="loan-text">Supprimer</span>
                            </button>
                        </>
                    );

                case "borrowed":
                case "emprunté":
                    return (
                        <button className="loan-button reserve-button" aria-label="Réserver ce livre">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                                <path d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.69 8.69a.75.75 0 1 0 1.06-1.061l-8.689-8.69a2.25 2.25 0 0 0-3.182 0l-8.69 8.69a.75.75 0 1 0 1.061 1.06l8.69-8.689Z" />
                                <path d="m12 5.432 8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 0-.75-.75h-3a.75.75 0 0 0-.75.75V21a.75.75 0 0 1-.75.75H5.625a1.875 1.875 0 0 1-1.875-1.875v-6.198a2.29 2.29 0 0 0 .091-.086L12 5.432Z" />
                            </svg>
                            <span className="loan-text">Réceptionner</span>
                        </button>
                    );
            }
        }

        // Pour les utilisateurs normaux, boutons basés sur le statut
        switch (status) {
            case "available":
            case "disponible":
                return (
                    <button className="loan-button borrow-button" aria-label="Emprunter ce livre">
                        <svg className="loan-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M12 17V7M12 17L17 12M12 17L7 12" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M4 21H20" strokeWidth="2" strokeLinecap="round" />
                        </svg>
                        <span className="loan-text">Emprunter</span>
                    </button>
                );

            case "borrowed":
            case "emprunté":
                return (
                    <button className="loan-button reserve-button" aria-label="Réserver ce livre">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                            <path d="M11.47 3.841a.75.75 0 0 1 1.06 0l8.69 8.69a.75.75 0 1 0 1.06-1.061l-8.689-8.69a2.25 2.25 0 0 0-3.182 0l-8.69 8.69a.75.75 0 1 0 1.061 1.06l8.69-8.689Z" />
                            <path d="m12 5.432 8.159 8.159c.03.03.06.058.091.086v6.198c0 1.035-.84 1.875-1.875 1.875H15a.75.75 0 0 1-.75-.75v-4.5a.75.75 0 0 0-.75-.75h-3a.75.75 0 0 0-.75.75V21a.75.75 0 0 1-.75.75H5.625a1.875 1.875 0 0 1-1.875-1.875v-6.198a2.29 2.29 0 0 0 .091-.086L12 5.432Z" />
                        </svg>
                        <span className="loan-text">Réserver</span>
                    </button>
                );

            case "reserved":
            case "réservé":
                return (
                    <button className="loan-button disabled-button" disabled aria-label="Livre réservé">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                            <path fillRule="evenodd" d="M12 1.5a5.25 5.25 0 0 0-5.25 5.25v3a3 3 0 0 0-3 3v6.75a3 3 0 0 0 3 3h10.5a3 3 0 0 0 3-3v-6.75a3 3 0 0 0-3-3v-3c0-2.9-2.35-5.25-5.25-5.25Zm3.75 8.25v-3a3.75 3.75 0 1 0-7.5 0v3h7.5Z" clipRule="evenodd" />
                        </svg>
                        <span className="loan-text">Réservé</span>
                    </button>
                );

            case "unavailable":
            case "indisponible":
                return (
                    <button className="loan-button disabled-button" disabled aria-label="Livre indisponible">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="loan-icon">
                            <path fillRule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clipRule="evenodd" />
                        </svg>
                        <span className="loan-text">Indisponible</span>
                    </button>
                );

            default:
                return (
                    <button className="loan-button disabled-button" disabled aria-label="Statut inconnu">
                        <span className="loan-text">Statut inconnu</span>
                    </button>
                );
        }
    };

    // Fonction pour obtenir la classe CSS du badge de statut
    const getStatusClass = (status: string) => {
        switch (status) {
            case "available":
            case "disponible":
                return "status-badge available";
            case "borrowed":
            case "emprunté":
                return "status-badge borrowed";
            case "reserved":
            case "réservé":
                return "status-badge reserved";
            case "unavailable":
            case "indisponible":
                return "status-badge unavailable";
            default:
                return "status-badge";
        }
    };

    return (
        <article className="book-card">
            <div className="book-cover">
                <img src={""} alt={book.titre} />
            </div>

            <div className="book-details">
                <header className="book-header">
                    <h2 className="book-title">{book.titre}</h2>
                    <p className="book-author">{book.auteur}</p>
                </header>

                <div className="book-meta">
                    <span className="book-year">{book.annee_publication}</span>
                    <span className="book-isbn">{book.isbn}</span>
                </div>
                <p className="book-description">{book.resume}</p>
            </div>

            <div className="book-actions">
                <span className={getStatusClass(status)}>{status}</span>
                {getActionButtons(status)}
            </div>
        </article>
    );
}