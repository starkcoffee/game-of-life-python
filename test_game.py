import pytest
from collections import namedtuple

A = 1
D = 0

class Board:

  def __init__(self, board_repr):
    self.board_repr = board_repr
  
  def get(self, x, y):
    return self.board_repr[y][x]

  def set(self, x, y, val):
    self.board_repr[y][x] = val

  def x_upper_bound(self):
    return len(self.board_repr[0])

  def y_upper_bound(self):
    return len(self.board_repr)

class Game:

  def __init__(self, matrix):
    self.board = Board(matrix)

  def list_neighbours(self, cell_cords):
    x, y = cell_cords
    neighbour_coords = [ (x+i, y+j) for i, j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] ]
    
    return [ self.board.get(i,j) for i,j in neighbour_coords 
      if i >= 0 and i < self.board.x_upper_bound() and j >=0 and j < self.board.y_upper_bound()
    ]

  def cell_should_die(self, cell_coords):
    return len([ neighbour for neighbour in self.list_neighbours(cell_coords) if neighbour == A ]) < 2

  def step(self):
    cells_to_be_killed = [(x,y) for y in range(self.board.y_upper_bound()) for x in range(self.board.x_upper_bound()) 
      if self.cell_should_die((x,y))]

    for x,y in cells_to_be_killed:
      self.board.set(x,y,D)

    return self.board.board_repr

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

def test_cell_should_die_if_has_less_than_two_neighbours():
  assert(Game([[A, A, A]]).cell_should_die((0,0))) == True
  assert(Game([[A, A, A]]).cell_should_die((1,0))) == False
  assert(Game([[A, A, A]]).cell_should_die((2,0))) == True

def test_game_is_initialised_with_board():
  assert(Game([[]]).board.board_repr) == [[]]
  
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
    ([[A],[A]], [[D],[D]]),
    ([[A,A,A]], [[D,A,D]]),
    ([[A],[A],[A]], [[D],[A],[D]]),
    ([[A, D], [A, A]], [[A, D], [A, A]]), 

  ]
)
def test_live_cells_with_fewer_than_two_neighbours_die(test_input, expected):
  assert(Game(test_input).step()) == expected

