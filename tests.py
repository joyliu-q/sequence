import random
from sequence import *

# TEST LOGIC BELOW 
class SequenceTest:
  def __init__(self):
    self.seq = Sequence()

  def make_moves(self, moves, switch_turn=True):
    random.shuffle(moves)
    for move in moves:
      self.seq.make_move(move)
      self.seq.check_winner(move)
      if switch_turn:
        self.seq.change_turn()

  def check_winner(self):
    # Test check_winner
    # Test 1: 5 in a row horizontally
    switch_turn = False
    self.seq.reset(switch_turn)
    moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == True

    # Test 2: 5 in a row vertically
    self.seq.reset(switch_turn)
    moves = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == True

    # Test 3: 5 in a row diagonally
    self.seq.reset(switch_turn)
    moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == True

    # Test 4: Multiple 5 in a row
    self.seq.reset(switch_turn)
    moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == True

    # Test 5: 5 in a row with corners
    self.seq.reset(switch_turn)
    moves = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == True

    # Test 6: No 5 in a row
    self.seq.reset(switch_turn)
    moves = [(1, 1), (3, 2), (2, 3), (4, 4), (5, 5)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == False

    # Test 7: 5 in a row but separate players
    switch_turn = True
    self.seq.reset(switch_turn)
    moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
    self.make_moves(moves, switch_turn)
    assert self.seq.has_winner() == False

    print("All tests passed for check_winner!")