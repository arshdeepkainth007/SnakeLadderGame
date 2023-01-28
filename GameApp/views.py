from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from random import randint
from rest_framework.parsers import JSONParser
from rest_framework import status as http_satus
from rest_framework.response import Response
from rest_framework.decorators import api_view

from SnakeLadderGame.pagination import StandardResultsSetPagination
from GameApp.models import Game, SNAKES, LADDERS, PLAYERS_POSITION_FIELDS, PLAYERS_NAME_FIELDS, PLAYERS_SWITCH
from GameApp.serializers import GameSerializer

# Create your views here.

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def GameAPI(request,game_id=None):
    response = {
        "data": None,
        "message": None
    }
    if request.method == 'GET':
        paginator = StandardResultsSetPagination()
        
        if not game_id:
            games = Game.objects.all()
            game_page = paginator.paginate_queryset(games, request)
            game_serializer = GameSerializer(game_page, many=True)
            return paginator.get_paginated_response(game_serializer.data)
        else:
            game_doc = Game.objects.get(GameID=game_id)
            game_serializer = GameSerializer(game_doc)
            response["data"] = game_serializer.data,
            response["message"] = "GET call successfull"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED) 

    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        game_serializer = GameSerializer(data = request_data)
        if game_serializer.is_valid(raise_exception=True):
            game_serializer.save()
            response["data"] = game_serializer.data
            response["message"] = "Added Successfully"
            return Response(response, status=http_satus.HTTP_202_ACCEPTED)
        response["message"] = "Failed to add"
        return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)

    elif request.method == 'PUT':
        game_doc = Game.objects.get(GameID=game_id)
        game_serializer = GameSerializer(game_doc)
        response = play_turn(game_doc),
        return Response(response, status=http_satus.HTTP_202_ACCEPTED)

    elif request.method == 'DELETE':
        if not game_id:
            response["message"] = "Please provide game id"
            return Response(response, status=http_satus.HTTP_406_NOT_ACCEPTABLE)
        game = Game.objects.get(GameID=game_id)
        game.delete()
        response["message"] = "Deleted game successfully"
        return Response(response, status=http_satus.HTTP_202_ACCEPTED)


def get_dice_values():
    value = randint(1,6)
    if value != 6:
        return [value]
    values = [value]
    count = 1
    while value == 6 and count < 3:
        count += 1
        value = randint(1,6)
        values.append(value)
    return values

def play_turn(game_doc):
    game_data = GameSerializer(game_doc).data
    response = {
        "data": None,
        "message": ""
    }
    curr_player = game_data.get("CurrPlayer")
    if curr_player == "0":
        response["data"] = None
        response["message"] = "Game has already finished"
    else:
        next_player = PLAYERS_SWITCH[curr_player]
        curr_player_name = game_data.get(PLAYERS_NAME_FIELDS[curr_player])
        next_player_name = game_data.get(PLAYERS_NAME_FIELDS[next_player])
        next_player_curr_position = game_data.get(PLAYERS_POSITION_FIELDS[next_player])
        dice_values = get_dice_values()
        curr_position = game_data.get(PLAYERS_POSITION_FIELDS[curr_player])
        new_position = curr_position + sum(dice_values)
        if new_position in SNAKES:
            response["message"] += f"Player {curr_player_name} got bit by snake at position {new_position}."
            new_position = SNAKES[new_position]
        elif new_position in LADDERS:
            response["message"] += f"Player {curr_player_name} got ladder at position {new_position}."
            new_position = LADDERS[new_position]
        if new_position >= 100:
            new_position = 100
            next_player_name = None
            game_data["CurrPlayer"] = "0"
            game_data["Winner"] = curr_player 
            response["message"] += f" Player {curr_player_name} WON the game! Hooray!"
        else:
            game_data["CurrPlayer"] = PLAYERS_SWITCH[curr_player]
            response["message"] += f" Player {curr_player_name} position now is {new_position}."
        game_data[PLAYERS_POSITION_FIELDS[curr_player]] = new_position

        game_serializer = GameSerializer(game_doc,data=game_data)
        if game_serializer.is_valid(raise_exception=True):
            game_serializer.save()

        response["data"] = {
            "Current Turn": curr_player_name,
            f"{curr_player_name}'s Current Position": curr_position,
            "Dice Throws": dice_values,
            f"{curr_player_name}'s New Position": new_position,
            "Next Turn": next_player_name,
            f"{next_player_name}'s Current Position": next_player_curr_position
        }
    return response
