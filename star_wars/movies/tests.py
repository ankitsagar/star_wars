# Django
from django.urls import reverse

# DRF
from rest_framework.test import APITestCase
from rest_framework import status

# App
from movies.services import MovieService
from users.services import UserService


class MovieListTestCase(APITestCase):
    fixtures = ['users.json', 'movies.json']

    def setUp(self):
        self.user_service = UserService()
        self.movie_service = MovieService()
        self.user = self.user_service.get_all().first()
        self.url = reverse(
            'movies:get_movies', kwargs={"user_id": self.user.id})
        self.invalid_user_url = reverse(
            'movies:get_movies', kwargs={"user_id": 999999999})

    def test_invalid_user(self):
        response = self.client.get(self.invalid_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_without_custom_name(self):
        movie = self.movie_service.get_all().first()
        response = self.client.get(self.url, {"query": movie.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_with_custom_name(self):
        movie = self.movie_service.get_all().first()
        user_movie = self.movie_service.create_or_update_user_metadata_entry(
            model_instance=movie,
            user=self.user,
            is_favorite=True,
            custom_name="some_random_name"
        )
        response = self.client.get(
            self.url, {"query": user_movie.custom_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_custom_movie_by_orignal_name(self):
        movie = self.movie_service.get_all().first()
        self.movie_service.create_or_update_user_metadata_entry(
            model_instance=movie,
            user=self.user,
            is_favorite=False,
            custom_name="some_random_name"
        )
        response = self.client.get(self.url, {"query": movie.title})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 0)


class UserMovieCreateTestCase(APITestCase):
    fixtures = ['users.json', 'movies.json']

    def setUp(self):
        self.user_service = UserService()
        self.movie_service = MovieService()
        self.user = self.user_service.get_all().first()
        self.movie = self.movie_service.get_all().first()
        self.url = reverse(
            'movies:create_user_movie',
            kwargs={"pk": self.movie.id}
        )
        self.invalid_movie_url = reverse(
            'movies:create_user_movie',
            kwargs={"pk": 9999999999}
        )

    def test_invalid_movie(self):
        response = self.client.post(
            self.invalid_movie_url,
            {
                "user": self.user.id,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_user(self):
        response = self.client.post(
            self.url,
            {
                "user": 99999999,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_movie_favourite(self):
        response = self.client.post(
            self.url,
            {
                "user": self.user.id,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_planet_favourite_with_custom_name(self):
        response = self.client.post(
            self.url,
            {
                "user": self.user.id,
                "is_favorite": True,
                "custom_name": "some random title"
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
