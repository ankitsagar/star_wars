# DRF
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

# App
from planets import constants
from planets.serializers import PlanetSerializer, UserPlanetCreateSerializer
from planets.services import PlanetService
from users.services import UserService


class GetPlanets(ListAPIView):
    serializer_class = PlanetSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.planet_service = PlanetService()

    def list(self, request, user_id, *args, **kwargs):
        query = request.query_params.get('query')
        # Validate given user id is correct
        user = self.user_service.get_user_by_id(user_id=user_id)
        if not user:
            raise NotFound(detail="user id not found")
        planet_queryset = self.planet_service.get_planets_with_user_planets(
            user=user, query=query)
        page = self.paginate_queryset(planet_queryset)
        serializer = self.serializer_class(page, many=True)
        response = self.get_paginated_response(serializer.data)
        return response


class CreateUserPlanet(UpdateAPIView):
    serializer_class = UserPlanetCreateSerializer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.planet_service = PlanetService()

    def put(self, request, planet_id, *args, **kwargs):
        planet = self.planet_service.get_planet_by_id(planet_id=planet_id)
        if not planet:
            raise NotFound(detail="planet id not found")

        serializer = self.serializer_class(
            data=request.data, context={constants.PLANET: planet}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
