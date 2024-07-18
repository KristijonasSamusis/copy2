from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Room, Player
from django.http import HttpResponse
from django.contrib import messages
import re
from .forms import NameForm


def index(request):

    form = NameForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            return redirect('create_room')
    else:
        pass


    context = {
        'rooms': Room.objects.all(),  # or however you are getting your rooms
        'form': form,

    }
    print("Kambariai", Room.objects.all())
    return render(request, "index.html", context)


def create_room(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['name']
            # Assuming a room is created here for the player
            room = Room.objects.create()  # Create a new room
            Player.objects.create(name=player_name, room=room)
        return redirect(f"/tic_tac/{room.id}/{player_name}/")
    else:
        form = NameForm()  # An unbound form
    # if form is not valid, redirect to form page with error messages
    return render(request, 'index.html', {'form': form})


def join_room(request):
    form = NameForm(request.POST or None)
    if form.is_valid():
        player_name = form.cleaned_data.get('name')
        room_id = request.POST.get("room-id", None)
        try:
            room = Room.objects.get(id=room_id)
            return redirect(f"/tic_tac/{room.id}/{player_name}/")
        except Room.DoesNotExist:
            messages.error(request, "Room does not exist.")
    # if form is not valid or room doesn’t exist, redirect appropriately
    return redirect('/')


def leave_room(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player.room = None  # remove player from old room
    player.save()  # apply changes to the database
    return HttpResponse("Player left the room successfully.")


def tic_tac(request, id=None, name=None):
    try:
        room = Room.objects.get(id=id)
        print("VARDAS", name)
        return render(request, "tic_tac.html", {"room": room, "name": name})
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist!!!")
        return redirect("/")


def tic_tac_name(request, id=None, name=None):
    print("VARDASNAME", name)
    return name
