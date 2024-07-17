from django.shortcuts import render, HttpResponse, redirect
from .models import Room
from django.contrib import messages
import re


# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html")
    elif request.method == "POST":
        room_id = request.POST.get("room-id", None)
        player_name = request.POST.get("player-name", "Unknown Player")
        if player_name == "":
            player_name = "Guest"
        if not re.match("^[a-zA-Z0-9]+$", player_name):
            messages.error(request, "Name should contain only alphabets and numbers.")
            return redirect("/")


        if(room_id):
            try:
                room = Room.objects.get(id=room_id)
                return redirect(f"/tic_tac/{room.id}/{player_name}/")
            except Room.DoesNotExist:
                messages.error(request, "Room does not exist.")
                return redirect("/")
        else:
            room = Room.objects.create()
            return redirect(f"/tic_tac/{room.id}/{player_name}/")
        return HttpResponse("post request handling")

def tic_tac(request, id=None, name=None):
    try:
        room = Room.objects.get(id=id)
        print("VARDAS", name)
        return render(request, "tic_tac.html", {"room": room, "name": name})
    except Room.DoesNotExist:
        messages.error(request, "Room does not exist!!!")
        return redirect("/")
    return render(request, "tic_tac.html")

def tic_tac_name(request, id=None, name=None):
    print("VARDASNAME", name)
    return name
# def your_view(request):
#     # Your existing view code...
#
#     # Generate ranges
#     rows = range(15)
#     cols = range(20)
#
#     # Pass ranges to template (combine with existing context if any)


    # return render(request, 'your_template.html', context)