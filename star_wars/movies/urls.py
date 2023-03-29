# Django
from django.urls import path

# App
from movies.views import GetMovies, CreateUserMovie


app_name = 'movies'

urlpatterns = [
    path('user/<int:user_id>/', GetMovies.as_view(), name="get_movies"),
    path(
        '<int:movie_id>/',
        CreateUserMovie.as_view(),
        name="create_user_movie"
    )
]
