from django.urls import path, include
from .views import tic_tac, index, create_room, join_room

urlpatterns = [
    path("", index, name='index'),
    path("tic_tac/<int:id>/<str:name>/", tic_tac),
    path('join_room/<int:room_id>/', join_room, name='join_room'),
    path('create_room/', create_room, name='create_room'),
]