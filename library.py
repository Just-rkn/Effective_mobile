import json
import os


class Library:
    """Класс для управления библиотекой книг."""

    __current_id: str = '1'

    def __init__(self, json_file: str) -> None:
        """Инициализация и загрузка книг из файла, если он существует."""

        self.__JSON_FILE = json_file
        self.__books: dict = self.__load_books()
        if self.__books:
            self.__current_id = str(max(map(int, self.__books.keys())) + 1)

    def __load_books(self) -> dict:
        """Загрузка книг из JSON файла, если он существует."""

        if os.path.exists(self.__JSON_FILE):
            try:
                with open(self.__JSON_FILE, 'r') as file:
                    books = json.load(file)
            except json.JSONDecodeError:
                books = {}
            return books
        return {}

    def __save_books(self) -> None:
        """Сохранение книг в JSON файл."""

        with open(self.__JSON_FILE, 'w') as file:
            json.dump(self.__books, file, indent=4)

    def add_book(self, title: str, author: str, year: str) -> dict:
        """Добавление книги в библиотеку."""

        book: dict = {
            'id': self.__current_id,
            'title': title,
            'author': author,
            'year': year,
            'status': 'в наличии'
        }
        self.__books[self.__current_id] = book
        self.__current_id = str(int(self.__current_id) + 1)
        self.__save_books()
        return book

    def delete_book(self, book_id: str) -> dict | None:
        """Удаление книги из библиотеки."""

        if book_id in self.__books:
            book = self.__books[book_id]
            del self.__books[book_id]
            self.__save_books()
            return book
        return None

    def search_books(self, **kwargs) -> list[dict]:
        """Поиск книг по заданным ключам и значения."""

        found_books: list[dict] = [
            book for book in self.__books.values()
            if all(
                book.get(key).lower() == value.lower()
                for key, value in kwargs.items()
            )
        ]

        return found_books

    def get_books(self) -> list[dict]:
        """Возвращает все книги из библиотеки."""

        return list(self.__books.values())

    def update_book_status(self, book_id: str, status: str) -> dict | None:
        """Обновление статуса книги из библиотеки."""

        if book_id in self.__books:
            self.__books[book_id]['status'] = status
            self.__save_books()
            return self.__books[book_id]
        return None


class LibraryManager:
    """Менеджер для взаимодействия с классом Library."""

    def __init__(self, json_file: str) -> None:
        """Инициализация класса Library."""

        self.__library = Library(json_file)

    @staticmethod
    def __get_book_info(book: dict) -> str:
        return (
            '\nКнига с полями:\n'
            f'название: {book["title"]}\n'
            f'автор: {book["author"]}\n'
            f'год: {book["year"]}\n'
            f'статус: {book["status"]}\n'
        )

    def __display_books(self, books: list[dict]):
        if books:
            for book in books:
                print(self.__get_book_info(book))
        else:
            print('Книги не найдены.')

    def add_book(self, title: str, author: str, year: str) -> None:
        """Добавляет книгу в библеотеку и выводит результат."""

        book: dict = self.__library.add_book(title, author, year)
        print(
            f'{self.__get_book_info(book)}'
            'успешно добавлена.\n'
        )

    def delete_book(self, book_id: str) -> None:
        """Удаляет книгу из библиотеки и выводит результат."""

        book: dict = self.__library.delete_book(book_id)
        if book:
            print(
                f'{self.__get_book_info(book)}'
                'успешно удалена.\n'
            )
        else:
            print('Книги с таким id не существует.')

    def search_books(self, **kwargs) -> None:
        """Ищет книгу по заданным параметрам и выводит результат."""

        books: list[dict] = self.__library.search_books(**kwargs)
        self.__display_books(books)

    def display_all_books(self):
        """Вывод всех книг."""

        books: list[dict] = self.__library.get_books()
        self.__display_books(books)

    def update_book_status(self, book_id: str, status: str) -> None:
        """Ищет книгу по id и обновляет ее статус."""

        book = self.__library.update_book_status(book_id, status)
        if book:
            print(
                f'{self.__get_book_info(book)}'
                'успешно изменена.'
            )
        else:
            print('Книги с таким id не существует.')
