import { API_URL } from "../../App";


export const BookService = {

    async getBooks() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Erreur réseau');
            return await response.json();
        } catch (error) {
            console.error("Erreur lors de la récupération des livres:", error);
            return [];
        }
    },

}