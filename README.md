# Azul board game clone

This is a text-based Python implementation of the fun, popular board game [Azul](https://boardgamegeek.com/boardgame/230802/azul).

If you are not familiar with the game, check out the [rules of the game](https://www.ultraboardgames.com/azul/game-rules.php) or watch [this brief video](https://www.youtube.com/watch?v=csJL-78NEPQ).

## Playing the game

Run the `azul.py` file.  For example

```python
$ python3 azul.py
```

### Instructions

It will prompt you for the number of players (between 2 and 4), and for the number of human players, if any.
If you only want to simulate a game with the AIs, enter 0.
For each human player it will prompt you for a name.

If only AIs are playing against each other, it will simulate the entire game. It will print out the AI's choices and the intermediate scores after each round.  At the end of the game, it will print out the player scores and the winner.

If one or more human players are playing, it will prompt you for your choices on each factory offer turn:
1. Pick a factory display or the center.  Enter your Choice Number as indicated on the screen.
2. Pick a color from the chosen tiles.
3. Pick a pattern line to place it on from the allowed lines indicated on the screen.  If the tiles can only be placed on one pattern line or on the floor, the game engine will automatically do so.

## Known Issues

1. No exception handling for improperly entered inputs.  The game engine will crash if you enter a wrong input which is not consistent with the stated prompt.

## Future plans

1. Add basic exception handling.
2. Currently the AIs choose randomly. Update the AIs to use some machine learning models.
3. Create a web or GUI based version of the game.