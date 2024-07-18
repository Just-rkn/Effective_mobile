import os

import unittest

from library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_books.json'
        self.library = Library(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        books_before = len(self.library.get_books())
        self.library.add_book('Test book', 'Test author', '2024')
        books_after = len(self.library.get_books())
        self.assertEqual(books_before, books_after - 1)
        last_book = self.library.get_books()[-1]
        self.assertEqual(last_book['title'], 'Test book')
        self.assertEqual(last_book['author'], 'Test author')
        self.assertEqual(last_book['year'], '2024')

    def test_delete_book(self):
        book_id = self.library.add_book('Test book', 'Test author', '2024')['id']
        books_before = len(self.library.get_books())
        self.library.delete_book(book_id)
        books_after = len(self.library.get_books())
        self.assertEqual(books_before, books_after + 1)

    def test_search_books(self):
        self.library.add_book('Search title', 'Search author', '2024')
        results = self.library.search_books(title='Search title', year='2024')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['author'], "Search author")
        self.assertEqual(results[0]['year'], '2024')

    def test_update_status(self):
        book_id = self.library.add_book('Test book', 'Test author', '2024')['id']
        self.library.update_book_status(book_id, 'выдана')
        book = self.library.get_books()[-1]
        self.assertEqual(book['status'], 'выдана')
