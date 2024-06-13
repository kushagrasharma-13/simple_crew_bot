from django.urls import path
from . import views

urlpatterns = [
    path('crew-requirements/', views.get_crew_requirements, name='get_crew_requirements'),
    path('healthcheck', views.health_check, name='health_check'),
]
