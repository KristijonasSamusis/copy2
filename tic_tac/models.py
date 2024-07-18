from django.db import models

# Create your models here.
class Room(models.Model):

    def __str__(self) -> str:
        return f"{self.id}"


class Player(models.Model):
    name = models.CharField(max_length=15)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name