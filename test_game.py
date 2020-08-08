import pytest
from collections import namedtuple

A = 0
D = 1

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

@pytest.mark.parametrize(
  "test_input, expected",
  [
    ([[D]], [[D]]),
    ([[D,D], [D,D]], [[D,D],[D,D]]),
  ]
)
def test_dead_cell_with_no_neighbours_stays_dead(test_input, expected):
  assert(Game(test_input).step()) == expected
  

