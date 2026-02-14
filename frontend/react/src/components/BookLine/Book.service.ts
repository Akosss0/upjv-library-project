import { API_URL } from "../../App";
import type { BookProps } from "./BookLine";


export const BookService = {

    async getBooks(): Promise<BookProps[]> {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Erreur réseau');
            return await response.json();
        } catch (error) {
            console.error("Erreur lors de la récupération des livres:", error);
            return [];
        }
    },

    async postBook(book: Omit<BookProps, 'livre_id'>): Promise<BookProps | null> {
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(book)
            });
            
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error("Erreur lors de la création du livre:", error);
            return null;
        }
    },

}