# App
from common.views import BaseUserMetaDataListView, BaseUserMetaDataCreateView
from planets import constants
from planets.serializers import PlanetSerializer, UserPlanetCreateSerializer
from planets.services import PlanetService


class GetPlanets(BaseUserMetaDataListView):
    serializer_class = PlanetSerializer
    model_service_class = PlanetService


class CreateUserPlanet(BaseUserMetaDataCreateView):
    serializer_class = UserPlanetCreateSerializer
    model_service_class = PlanetService
    not_found_error = "planet id not found"
    instance_context_key = constants.PLANET
