from library import LibraryManager


def main():
    """Функция для отображения интерфейса библеотеки."""

    library: LibraryManager = LibraryManager()

    print(
        '\nМеню:',
        '1. Добавить книгу',
        '2. Удалить книгу',
        '3. Искать книги',
        '4. Показать все книги',
        '5. Обновить статус книги',
        '6. Выход',
        sep='\n'
    )

    while True:
        choice: str = input('Введите номер действия: ')

        match choice:
            case '1':
                title: str = input('Введите название книги: ')
                author: str = input('Введите автора книги: ')
                year: str = input('Введите год издания: ')
                library.add_book(title, author, year)
            case '2':
                book_id: str = input('Введите ID книги для удаления: ')
                library.delete_book(book_id)
            case '3':
                query: str = input(
                    'Введите параметры для поиска в формате "ключ=значение"'
                )
                try:
                    kwargs: dict = dict(
                        map(lambda x: tuple(x.split('=')), query.split())
                    )
                    library.search_books(**kwargs)
                except Exception:
                    print('Неверно указаны параметры.')
            case '4':
                library.display_all_books()
            case '5':
                book_id: str = input('Введите ID книги для обновления: ')
                status: str = input(
                    'Введите новый статус (в наличии/выдана): '
                )
                if status not in ('в наличии', 'выдана'):
                    print(
                        'Неверный статус. Допустимые значения:'
                        '"в наличии" или "выдана".'
                    )
                    continue
                library.update_book_status(book_id, status)
            case '6' | 'exit' | 'exit()':
                break
            case _:
                print('Неверный выбор, попробуйте еще раз.')


if __name__ == '__main__':
    main()
