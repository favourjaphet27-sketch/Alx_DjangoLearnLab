from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from api.models import Book


class BookAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.login(username="testuser", password="testpass123")

        # Main book for tests
        self.main_book = Book.objects.create(
            title="Normal People", author="Sally Rooney", publication_year=2018
        )

        # Secondary book for search and ordering tests
        self.second_book = Book.objects.create(
            title="Conversations With Friends",
            author="Sally Rooney",
            publication_year=2017,
        )

    def test_list_books(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

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
        self.assertTrue(len(response.data) >= 2)
