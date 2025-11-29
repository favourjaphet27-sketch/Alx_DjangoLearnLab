from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import Book


class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user for authentication
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Main book for tests
        self.main_book = Book.objects.create(
            title="Normal People", author="Sally Rooney", publication_year=2018
        )

        # Additional book for search/filter/order
        self.second_book = Book.objects.create(
            title="Crime and Punishment",
            author="Fyodor Dostoevsky",
            publication_year=1866,
        )

    def test_list_books(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)

    def test_retrieve_single_book(self):
        response = self.client.get(f"/books/{self.main_book.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Normal People")

    def test_create_book(self):
        data = {
            "title": "New Book Test",
            "author": "Test Author",
            "publication_year": 2020,
        }
        response = self.client.post("/books/create/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "New Book Test")

    def test_update_book(self):
        data = {
            "title": "Normal People Updated",
            "author": "Sally Rooney",
            "publication_year": 2018,
        }
        response = self.client.put(f"/books/update/{self.main_book.id}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Normal People Updated")

    def test_delete_book(self):
        response = self.client.delete(f"/books/delete/{self.main_book.id}/")
        self.assertEqual(response.status_code, 204)

    def test_search_books(self):
        response = self.client.get("/books/?search=Normal")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Normal People")

    def test_ordering_books(self):
        response = self.client.get("/books/?ordering=publication_year")
        self.assertEqual(response.status_code, 200)
