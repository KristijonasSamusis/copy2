from django.urls import path, include
from .views import tic_tac, index

urlpatterns = [
    path("", index),
    path("tic_tac/<int:id>/<str:name>/", tic_tac),
]