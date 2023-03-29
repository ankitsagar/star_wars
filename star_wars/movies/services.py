# App
from common.services import BaseServiceWithUserMedataModel
from movies import constants
from movies.models import Movie, UserMovie


class MovieService(BaseServiceWithUserMedataModel):
    model = Movie
    model_name_field = "title"
    model_id_field_in_user_metatdata = "movie_id"
    model_field_in_user_metadata = "movie"
    user_level_metadata_model = UserMovie
    user_level_metadata_rel_name = constants.MOVIE_TO_USER_REL
    user_level_metadata_attr_name = constants.USER_MOVIE_ATTR
