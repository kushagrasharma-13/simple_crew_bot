from django.urls import path
from . import views

urlpatterns = [
    path('crew-requirements/', views.get_crew_requirements, name='get_crew_requirements'),
]
