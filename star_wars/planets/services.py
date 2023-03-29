# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch, Q

# App
from planets.models import Planet, UserPlanet


class PlanetService:

    def __init__(self):
        self.user_planet_service = UserPlanetService()

    def get_planet_by_id(self, planet_id):
        try:
            planet = Planet.objects.get(id=planet_id)
        except ObjectDoesNotExist:
            planet = None
        return planet

    def get_all_planets(self):
        return Planet.objects.all()

    def bulk_create(self, planets_data):
        objs = []
        fields = [field.name for field in Planet._meta.get_fields()]
        for planet_data in planets_data:
            for key in list(planet_data.keys()):
                if key not in fields:
                    planet_data.pop(key)
            objs.append(Planet(**planet_data))
        Planet.objects.bulk_create(objs=objs)

    def get_planets_with_user_planets(self, user, query=None):
        """
        Fetches all the planets with user planets table if there are user
        planet entry.
        """
        filter_args = []
        if query:
            user_planet_queryset = self.user_planet_service.get_user_planets(
                user_id=user.id, query=query
            )
            # These are the found planet ids which need to be included in the
            # result
            found_planet_ids = [
                user_planet.planet_id
                for user_planet in user_planet_queryset
            ]

            # We need all user's planet to avoid searching in planet table
            user_planet_ids = self.user_planet_service.get_planet_ids_from_user_planet(  # noqa
                user.id)

            # We need to apply a filter on planet table when the name contains
            # the query then it must not be the part of user planet table and
            # inculde all the search results from user planet table
            filter_args.append(
                (Q(name__icontains=query) & ~Q(id__in=user_planet_ids))
                | Q(id__in=found_planet_ids)
            )
        else:
            user_planet_queryset = self.user_planet_service.get_user_planets(
                user_id=user.id
            )

        planets = Planet.objects.prefetch_related(
            Prefetch(
                'user_planets',
                to_attr='user_planet',
                queryset=user_planet_queryset
            )
        ).filter(*filter_args)
        return planets


class UserPlanetService:

    def get_user_planet(self, user_id, planet_id):
        try:
            user_planet = UserPlanet.objects.get(
                user_id=user_id, planet_id=planet_id)
        except ObjectDoesNotExist:
            user_planet = None
        return user_planet

    def get_user_planets(self, user_id, query=None):
        """ Return all the planets related to the user """
        queryset = UserPlanet.objects.filter(user_id=user_id)
        if query:
            queryset = queryset.filter(custom_name__icontains=query)
        return queryset

    def create_or_update_user_planet(
            self, planet, user, is_favorite, custom_name=None):
        user_planet = self.get_user_planet(user.id, planet.id)
        if not user_planet:
            user_planet = UserPlanet(user=user, planet=planet)
        user_planet.is_favorite = is_favorite
        # If custom name is none then attach the orignal name
        user_planet.custom_name = custom_name or planet.name
        user_planet.save()
        return user_planet

    def get_planet_ids_from_user_planet(self, user_id):
        return self.get_user_planets(user_id).values_list(
            "planet_id", flat=True)
