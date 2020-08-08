from collections import namedtuple

class Game:

  def __init__(self, board):
    self.board = board

  def step(self):
    return self.board

def test_game_is_initialised_with_board():
  assert(Game([[]]).board) == [[]]
  
def test_game_returns_board_after_step():
  game = Game([[]])
  assert(game.step()) == [[]]
