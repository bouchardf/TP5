from enum import Enum

class GameState(Enum):
   NOT_STARTED = 0
   ROUND_ACTIVE = 1
   ROUND_DONE = 2
   GAME_OVER = 3
   PLAYER_WON = 4
   COMPUTER_WON = 5