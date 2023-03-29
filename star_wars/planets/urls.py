# Django
from django.urls import path

# App
from planets.views import CreateUserPlanet, GetPlanets

app_name = 'planets'

urlpatterns = [
    path('user/<int:user_id>/', GetPlanets.as_view(), name="get_planets"),
    path(
        '<int:planet_id>/',
        CreateUserPlanet.as_view(),
        name="create_user_planet")
]
