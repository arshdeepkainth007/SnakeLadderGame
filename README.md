# The Snake Ladder Game
#### This is a django based python prototype of the snake ladder game where two players have to cross the board of snakes and ladders. 
#### The fastest one to reach the end wins

## Technologies used:
#### Python Django
#### MySQL in local
#### Postman for api testing
#### Github for source control

## Game Board
![board_image](https://user-images.githubusercontent.com/38393402/215291182-3f830820-f793-41bd-912f-6b1deab54e1b.png)
## Rules of the Game
#### 1. Each Player starts at 0
#### 2. The quickest one to reach 100 wins
#### 3. Each Player gets alternate turns of throwing dice (1 to 6)
#### 4. If 6 comes on dice, the player gets to rethrow the dice (max 3 times)
#### 5. If the player reaches at the bottom of a ladder, it advances to the ladder's top (ex. 28 -> 84)
#### 6. If the player reaches at the mouth of a snake, it retreats to the snake's tail (ex. 87 -> 36)

## APIs:
### 1. Initiate a game
```
curl --location --request POST 'http://127.0.0.1:8000/games' \
--header 'Content-Type: application/json' \
--data-raw '{
    "P1Name": "Samar",
    "P2Name": "Vikram"
}'
```
#### This api initiates a game between `P1Name` and `P2Name`, the response provides with `GameID` that is used to play the game.
#### Sample response:
```
{
    "data": {
        "GameID": 4,
        "P1Name": "Samar",
        "P2Name": "Vikram",
        "Winner": "0",
        "CurrPlayer": "1",
        "P1Pos": 0,
        "P2Pos": 0
    },
    "message": "Added Successfully"
}
```

### 2. Play the game
```
curl --location --request PUT 'http://127.0.0.1:8000/games/4/'
```
#### This api throws the dice and evaluates the new position of the current player who was playing, also, will inform of the other player's current position.
#### In case the current player got a 6, he get's one more changes at dice and the compound value is used to advance the position.
```
{
        "data": {
            "Current Turn": "Vikram",
            "Vikram's Current Position": 0,
            "Dice Throws": [
                6,
                5
            ],
            "Vikram's New Position": 11,
            "Next Turn": "Samar",
            "Samar's Current Position": 5
        },
        "message": " Player Vikram is now at 11."
    }
```

#### Whenever a player is bit by snake or got a ladder, the same is reflected in `message` field, as shown below.

```
{
        "data": {
            "Current Turn": "Vikram",
            "Vikram's Current Position": 15,
            "Dice Throws": [
                2
            ],
            "Vikram's New Position": 7,
            "Next Turn": "Samar",
            "Samar's Current Position": 11
        },
        "message": "Player Vikram got bit by snake at 17. Player Vikram is now at 7."
    }
```

#### Once a player reaches 100, he/she wins, and we get the following response.

```
{
        "data": {
            "Current Turn": "Samar",
            "Samar's Current Position": 99,
            "Dice Throws": [
                5
            ],
            "Samar's New Position": 100,
            "Next Turn": null,
            "None's Current Position": 68
        },
        "message": " Player Samar WON the game! Hooray!"
    }
```

#### If we try to use the same api again to play turn at a game that's completed, we get the following response.
```
{
        "data": null,
        "message": "Game has already finished"
    }
]
```
#### All the feedback is welcomed.
## Thank You
