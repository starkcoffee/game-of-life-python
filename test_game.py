from collections import namedtuple

class Game:

  def __init__(self, board):
    self.board = board

def test_game_is_initialised_with_board():
    assert(Game([[]]).board) == [[]]
  
