from django.db import models

# Create your models here.

PLAYERS = {
    ("0", "None"),
    ("1", "Player1"),
    ("2", "Player2")
}

PLAYERS_POSITION_FIELDS = {
    "1": "P1Pos",
    "2": "P2Pos"
}

PLAYERS_NAME_FIELDS = {
    "1": "P1Name",
    "2": "P2Name"
}

PLAYERS_SWITCH = {
    "1": "2",
    "2": "1"
}

LADDERS = {
    1: 38,
    4: 14,
    9: 31,
    21: 42,
    28: 84,
    51: 67,
    72: 91,
    80: 99,
}

SNAKES = {
    17: 7,
    54: 34,
    62: 19,
    64: 60,
    87: 36,
    92: 73,
    95: 75,
    98: 79
}

class Game(models.Model):
    GameID = models.AutoField(primary_key=True)
    P1Name = models.CharField(max_length=256, default="player_1")
    P2Name = models.CharField(max_length=256, default="player_2")
    Winner = models.CharField(max_length=1, choices=PLAYERS, default='0')
    CurrPlayer = models.CharField(max_length=256, choices=PLAYERS, default='1')
    P1Pos = models.IntegerField(default=0)
    P2Pos = models.IntegerField(default=0)

