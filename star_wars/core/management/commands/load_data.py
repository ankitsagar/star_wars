# Django imports
from django.conf import settings
from django.core.management.base import BaseCommand

# App imports
from movies.services import MovieService
from planets.services import PlanetService

# Other imports
import requests


class Command(BaseCommand):
    """ Management command to load all movies and planets """

    def _fetch_data(self, url):
        """
        Does the iterative call on the API till we get all the data
        """
        entire_data = []
        page = 1
        params = {"page": page}
        response = requests.get(url, params=params)
        while response.status_code == 200:
            print(response.status_code, params)
            data = response.json()
            entire_data.append(data["results"])
            # Then it's the last page
            if data['next'] is None:
                break
            page += 1
            params["page"] = page
            response = requests.get(url, params=params)
        return entire_data

    def _load_planets(self):
        planet_service = PlanetService()
        planet_url = settings.SW_API_BASE_URL + settings.SW_PLANETS_ENDPOINT
        planets_data = self._fetch_data(planet_url)
        for data in planets_data:
            planet_service.bulk_create(data)

    def _load_movies(self):
        movie_service = MovieService()
        movie_url = settings.SW_API_BASE_URL + settings.SW_MOVIES_ENDPOINT
        movies_data = self._fetch_data(movie_url)
        for data in movies_data:
            movie_service.bulk_create(data)

    def handle(self, *args, **options):
        self.stdout.write('Loading Planets.....')
        self._load_planets()
        self.stdout.write('====== Planets Dumped ======')
        self.stdout.write('Loading movies.....')
        self._load_movies()
        self.stdout.write('====== Movies Dumped ======')
