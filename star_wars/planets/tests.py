# Django
from django.urls import reverse

# DRF
from rest_framework.test import APITestCase
from rest_framework import status

# App
from users.services import UserService
from planets.services import PlanetService


class PlanetListTestCase(APITestCase):
    fixtures = ['users.json', 'planets.json']

    def setUp(self):
        self.user_service = UserService()
        self.planet_service = PlanetService()
        self.user = self.user_service.get_all().first()
        self.url = reverse(
            'planets:get_planets', kwargs={"user_id": self.user.id})
        self.invalid_user_url = reverse(
            'planets:get_planets', kwargs={"user_id": 999999999})

    def test_invalid_user(self):
        response = self.client.get(self.invalid_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_without_custom_name(self):
        planet = self.planet_service.get_all().first()
        response = self.client.get(self.url, {"query": planet.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_with_custom_name(self):
        planet = self.planet_service.get_all().first()
        user_planet = self.planet_service.create_or_update_user_metadata_entry(
            model_instance=planet,
            user=self.user,
            is_favorite=True,
            custom_name="some_random_name"
        )
        response = self.client.get(
            self.url, {"query": user_planet.custom_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_search_custom_planet_by_orignal_name(self):
        planet = self.planet_service.get_all().first()
        self.planet_service.create_or_update_user_metadata_entry(
            model_instance=planet,
            user=self.user,
            is_favorite=False,
            custom_name="some_random_name"
        )
        response = self.client.get(self.url, {"query": planet.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 0)


class UserPlanetCreateTestCase(APITestCase):
    fixtures = ['users.json', 'planets.json']

    def setUp(self):
        self.user_service = UserService()
        self.planet_service = PlanetService()
        self.user = self.user_service.get_all().first()
        self.palnet = self.planet_service.get_all().first()
        self.url = reverse(
            'planets:create_user_planet',
            kwargs={"pk": self.palnet.id}
        )
        self.invalid_planet_url = reverse(
            'planets:create_user_planet',
            kwargs={"pk": 9999999999}
        )

    def test_invalid_planet(self):
        response = self.client.put(
            self.invalid_planet_url,
            {
                "user": self.user.id,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_user(self):
        response = self.client.put(
            self.url,
            {
                "user": 99999999,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_set_planet_favourite(self):
        response = self.client.put(
            self.url,
            {
                "user": self.user.id,
                "is_favorite": True,
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_planet_favourite_with_custom_name(self):
        response = self.client.put(
            self.url,
            {
                "user": self.user.id,
                "is_favorite": True,
                "custom_name": "some random planet"
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
