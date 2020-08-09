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

  def within_bounds(self, x, y):
    return x >= 0 and x < self.x_upper_bound() and y >=0 and y < self.y_upper_bound()

class Game:

  def __init__(self, matrix):
    self.board = Board(matrix)

  def list_neighbour_values(self, x, y):
    relative_coords = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] 
    neighbour_coords = [ (x+i, y+j) for i, j in relative_coords ]
    
    return [ self.board.get(*coord) for coord in neighbour_coords if self.board.within_bounds(*coord) ]

  def cell_should_die(neighbours):
    return neighbours.count(A) < 2 or neighbours.count(A) > 3 

  def step(self):
    cells_to_be_killed = [ (x,y) 
      for x in range(self.board.x_upper_bound()) 
      for y in range(self.board.y_upper_bound()) 
      if Game.cell_should_die(self.list_neighbour_values(x,y))
    ]

    for x,y in cells_to_be_killed:
      self.board.set(x,y,D)

    return self.board.board_repr

## UNIT TESTS

def test_game_is_initialised_with_board():
  assert(Game([[]]).board.board_repr) == [[]]
  
def test_game_returns_board_after_step():
  game = Game([[]])
  assert(game.step()) == [[]]

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
    ([[D, A], [A, D], [D, D]], (0, 0), [D, A, A]),
    ([[D, A], [A, D], [D, D]], (0, 1), [D, D, D, D, A]),
    ([[D, A], [A, D], [D, D]], (1, 1), [D, D, D, A, A]),
    ([[D, A], [A, D], [D, D]], (2, 1), [D, D, A]),
  ]
)
def test_returns_neighbours(board, cell_coords, expected):
  assert(sorted(Game(board).list_neighbour_values(*cell_coords))) == expected

def test_cell_should_die_if_has_less_than_two_or_greater_than_three_live_neighbours():
  assert(Game.cell_should_die([])) == True
  assert(Game.cell_should_die([A])) == True
  assert(Game.cell_should_die([D,D])) == True
  assert(Game.cell_should_die([D,A,D])) == True
  assert(Game.cell_should_die([A,A])) == False
  assert(Game.cell_should_die([A,A,A])) == False
  assert(Game.cell_should_die([A,A,A,A])) == True
  assert(Game.cell_should_die([A,A,A,A,A,D,D,D])) == True


## INTEGRATION TESTS

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

