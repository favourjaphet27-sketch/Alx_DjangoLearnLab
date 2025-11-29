from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Book


class TestBookAPI(APITestCase):
    def setUp(self):
        # Create two books for testing
        self.book1 = Book.objects.create(
            title="Crime and Punishment",
            author="Fyodor Dostoevsky",
            publication_year=1866,
        )
        self.book2 = Book.objects.create(
            title="Normal People", author="Sally Rooney", publication_year=2018
        )

        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Crime and Punishment")

    def test_create_book(self):
        data = {"title": "Test Book", "author": "Test Author", "publication_year": 2024}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        data = {"title": "Crime & Punishment Revised"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Crime & Punishment Revised")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)
