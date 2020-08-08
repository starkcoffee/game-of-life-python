import pytest
from collections import namedtuple

A = 0
D = 1

class Game:

  def __init__(self, board):
    self.board = board

  def step(self):
    # for each cell, if it is alive, if it has fewer than 2 neighbours, then make it a dead cell
    for row in self.board:
      for col, cell in enumerate(row):
        if cell == A:
          row[col] = D

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
  
@pytest.mark.parametrize(
  "test_input, expected",
  [
    ([[A]], [[D]]),
  ]
)

def test_live_cells_with_fewer_than_two_neighbours_die(test_input, expected):
  assert(Game(test_input).step()) == expected
