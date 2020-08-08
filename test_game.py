import pytest
from collections import namedtuple

A = 1
D = 0

class Game:

  def __init__(self, board):
    self.board = board

  def list_neighbours(self, cell_cords):
    x, y = cell_cords
    neighbour_coords = [ (x+i, y+j) for i, j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] ]
    
    return [ self.board[j][i] for i,j in neighbour_coords 
      if i >= 0 and i < len(self.board[0]) and  j >=0 and j < len(self.board) 
    ]

  def cell_should_die(self, cell_coords):
    return len([ neighbour for neighbour in self.list_neighbours(cell_coords) if neighbour == A ]) < 2

  def step(self):
    for y, row in enumerate(self.board):
      for x, cell in enumerate(row):
        if cell == A and self.cell_should_die((x, y)):
          row[x] = D

    return self.board

@pytest.mark.parametrize(
  "board, cell_coords, expected",
  [
    ([[]], (42, 42), []),
    ([[A]], (0, 0), []),
    ([[D, A, D]], (0, 0), [A]),
    ([[D, A, D]], (1, 0), [D, D]),
    ([[D, A, D]], (2, 0), [A]),
    ([[D], [A], [D]], (0, 0), [A]),
    ([[D], [A], [D]], (0, 1), [D, D]),
    ([[D], [A], [D]], (0, 2), [A]),
  ]
)
def test_returns_neighbours(board, cell_coords, expected):
  assert(Game(board).list_neighbours(cell_coords)) == expected

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
    ([[A,A]], [[D, D]]),
    ([[A,A,A]], [[D,A,D]]),
  ]
)
@pytest.mark.skip
def test_live_cells_with_fewer_than_two_neighbours_die(test_input, expected):
  assert(Game(test_input).step()) == expected
