# App
from common.services import BaseServiceWithUserMedataModel
from planets import constants
from planets.models import Planet, UserPlanet


class PlanetService(BaseServiceWithUserMedataModel):
    model = Planet
    model_name_field = "name"
    model_id_field_in_user_metatdata = "planet_id"
    model_field_in_user_metadata = "planet"
    user_level_metadata_model = UserPlanet
    user_level_metadata_rel_name = constants.PLANET_TO_USER_REL
    user_level_metadata_attr_name = constants.USER_PLANET_ATTR
