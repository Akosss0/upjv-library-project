import { useEffect, useState } from "react";

import { Header } from "../components/Header/Header";
import { List } from "../components/List/List";
import { BookService } from "../components/BookLine/Book.service";
import { BookLine, type BookProps } from "../components/BookLine/BookLine";


export function Home() {
    const [books, setBooks] = useState<BookProps[]>([]);

    useEffect(() => {
        BookService.getBooks().then(data => setBooks(data));
    }, []);

    console.log(books)

    /* const mockBook: BookProps[] = [{
        id: 1,
        title: "Le Petit Prince",
        author: "Antoine de Saint-Exupéry",
        description: "Un conte philosophique.",
        year: 1943,
        isbn: "978-2070612758",
        cover: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHOpD8bvVfGOjLGwVMyUwlk_c-y-GpufiWJw&s",
        status: "réservé",
    }]; */


    return (
        <>
            <Header></Header>
            <List>
                {books.map(book => <BookLine book={book}></BookLine>)}
            </List>
        </>
    );
}