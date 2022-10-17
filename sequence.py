from cards import Suit, Card, Deck
from agents import *
import random, time
import os
from utils import ANSIText

ansi = ANSIText()

class Cell:
  def __init__(self, card):
    self.card = card
    self.occupied = None # occupied is either None, Green (0), or Blue (1), or Both (2)

  def get_card(self):
    return self.card
  
  def claim(self, player):
    if player != 0 and player != 1 and player != 2:
      return
    self.occupied = player

  def unclaim(self): # If there's a one-eye jack
    self.occupied = None

  def is_occupied(self):
    return self.occupied != None
  
  def __str__(self):
    if self.occupied == 0:
      return ansi.green('00')
    elif self.occupied == 1:
      return ansi.red('11')
    elif self.occupied == 2:
      return ansi.purple('**')
    else:
      return ansi.cyan(str(self.card))

# Sequence game class
class Sequence:

  CARD_POSITIONS = [
      [Card(0, Suit.SPADE), Card(2, Suit.SPADE), Card(3, Suit.SPADE), Card(4, Suit.SPADE), Card(5, Suit.SPADE), Card(6, Suit.SPADE), Card(7, Suit.SPADE), Card(8, Suit.SPADE), Card(9, Suit.SPADE), Card(0, Suit.SPADE)],
      [Card(6, Suit.CLUB), Card(5, Suit.CLUB), Card(4, Suit.CLUB), Card(3, Suit.CLUB), Card(2, Suit.CLUB), Card(1, Suit.HEART), Card(13, Suit.HEART), Card(12, Suit.HEART), Card(10, Suit.HEART), Card(10, Suit.SPADE)],
      [Card(7, Suit.CLUB), Card(1, Suit.SPADE), Card(2, Suit.DIAMOND), Card(3, Suit.DIAMOND), Card(4, Suit.DIAMOND), Card(5, Suit.DIAMOND), Card(6, Suit.DIAMOND), Card(7, Suit.DIAMOND), Card(9, Suit.HEART), Card(12, Suit.SPADE)],
      [Card(8, Suit.CLUB), Card(13, Suit.SPADE), Card(6, Suit.CLUB), Card(5, Suit.CLUB), Card(4, Suit.CLUB), Card(3, Suit.CLUB), Card(2, Suit.CLUB), Card(8, Suit.DIAMOND), Card(8, Suit.HEART), Card(13, Suit.SPADE)],
      [Card(9, Suit.CLUB), Card(12, Suit.SPADE), Card(7, Suit.CLUB), Card(6, Suit.HEART), Card(5, Suit.HEART), Card(4, Suit.HEART), Card(1, Suit.HEART), Card(9, Suit.DIAMOND), Card(7, Suit.HEART), Card(1, Suit.SPADE)],
      [Card(10, Suit.CLUB), Card(10, Suit.SPADE), Card(8, Suit.CLUB), Card(7, Suit.HEART), Card(2, Suit.HEART), Card(3, Suit.HEART), Card(13, Suit.HEART), Card(10, Suit.DIAMOND), Card(6, Suit.HEART), Card(2, Suit.DIAMOND)],
      [Card(12, Suit.CLUB), Card(9, Suit.SPADE), Card(9, Suit.CLUB), Card(8, Suit.HEART), Card(9, Suit.HEART), Card(10, Suit.HEART), Card(12, Suit.HEART), Card(12, Suit.DIAMOND), Card(5, Suit.HEART), Card(3, Suit.DIAMOND)],
      [Card(13, Suit.CLUB), Card(8, Suit.SPADE), Card(10, Suit.CLUB), Card(12, Suit.CLUB), Card(13, Suit.CLUB), Card(1, Suit.CLUB), Card(1, Suit.DIAMOND), Card(13, Suit.DIAMOND), Card(4, Suit.HEART), Card(4, Suit.DIAMOND)],
      [Card(1, Suit.CLUB), Card(7, Suit.SPADE), Card(6, Suit.SPADE), Card(5, Suit.SPADE), Card(4, Suit.SPADE), Card(3, Suit.SPADE), Card(2, Suit.SPADE), Card(2, Suit.HEART), Card(3, Suit.HEART), Card(5, Suit.DIAMOND)],
      [Card(0, Suit.SPADE), Card(1, Suit.DIAMOND), Card(13, Suit.DIAMOND), Card(12, Suit.DIAMOND), Card(10, Suit.DIAMOND), Card(9, Suit.DIAMOND), Card(8, Suit.DIAMOND), Card(7, Suit.DIAMOND), Card(6, Suit.DIAMOND), Card(0, Suit.SPADE)]
    ]

  def __init__(self, switch_turn=True):
    self.board = [[Cell(c) for c in row] for row in Sequence.CARD_POSITIONS]
    self.height = len(self.board)
    self.width = len(self.board[0])
    self.board[0][0].claim(2)
    self.board[-1][0].claim(2)
    self.board[0][-1].claim(2)
    self.board[-1][-1].claim(2)
    self.players = [RandAgent(), RandAgent()]
    self.turn = 0
    self.fives = [0, 0] # [Green, Blue]
    self.switch_turn = switch_turn
    self.last_move = None
    self.deck = Deck(2, jokers=False, shuffle=True)
    self.hands = [[], []]
    for _ in range(7):
      self.hands[0].append(self.deck.draw())
      self.hands[1].append(self.deck.draw())
    
  def get_hand(self, player):
    return self.hands[player]

  def make_move(self, position):
    # If winner is already decided, don't allow any more moves
    if self.has_winner():
      return
    # Otherwise, make the move
    row, col = position
    if row < 0 or row >= self.height or col < 0 or col >= self.width:
      return False
    if self.board[row][col].is_occupied():
      return False
    self.board[row][col].claim(self.turn)
    self.hands[self.turn].append(self.deck.draw())
    self.last_move = position
    return True

  def check_winner(self, position): # given that the current move is made, is there a winner
    if position == None:
      return False
    row_offset = [(0, -4), (0, -3), (0, -2), (0, -1), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    col_offset = [(-4, 0), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    diag_offset = [(-4, -4), (-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

    row, col = position

    row_acc = 0
    # In all tiles in row offset, if there's any consecutive 5 of the same occupied, increment by 1
    for offset in row_offset:
      new_pos = (row + offset[0], col + offset[1])
      if new_pos[0] < 0 or new_pos[0] >= self.height or new_pos[1] < 0 or new_pos[1] >= self.width:
        continue
      if self.board[new_pos[0]][new_pos[1]].occupied == self.turn or self.board[new_pos[0]][new_pos[1]].occupied == 2:
        row_acc += 1
        if row_acc == 5:
          self.fives[self.turn] += 1
      else:
        row_acc = 0
    
    col_acc = 0
    for offset in col_offset:
      new_pos = (row + offset[0], col + offset[1])
      if new_pos[0] < 0 or new_pos[0] >= self.height or new_pos[1] < 0 or new_pos[1] >= self.width:
        continue
      if self.board[new_pos[0]][new_pos[1]].occupied == self.turn or self.board[new_pos[0]][new_pos[1]].occupied == 2:
        col_acc += 1
        if col_acc == 5:
          self.fives[self.turn] += 1
      else:
        col_acc = 0
    
    diag_acc = 0
    for offset in diag_offset:
      new_pos = (row + offset[0], col + offset[1])
      if new_pos[0] < 0 or new_pos[0] >= self.height or new_pos[1] < 0 or new_pos[1] >= self.width:
        continue
      if self.board[new_pos[0]][new_pos[1]].occupied == self.turn or self.board[new_pos[0]][new_pos[1]].occupied == 2:
        diag_acc += 1
        if diag_acc == 5:
          self.fives[self.turn] += 1
      else:
        diag_acc = 0

    return self.has_winner()
  
  # State retrieval functions 
  def has_winner(self):
    return self.get_winner() != None

  def get_winner(self):
    if self.fives[0] >= 2:
      return 0
    elif self.fives[1] >= 2:
      return 1
    else:
      return None
  
  def change_turn(self):
    self.turn = int(not self.turn)

  def count_occupied(self, card):
    count = 0
    for row in self.board:
      for cell in row:
        if cell.is_occupied() and cell.card == card:
          count += 1
    return count

  def check_unneeded_cards(self, player):
    return [card for card in self.hands[player] if self.count_occupied(card) >= 2]

  def render(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Turn: ", self.turn)
    print(str(self), end='\r')
    time.sleep(0.5)
  
  def __str__(self):
    out = ''
    for row in self.board:
      out += ' '.join(map(str, row)) + '\n'
    return out

  def play(self):
    self.render()
    while not self.has_winner():
      unneeded = self.check_unneeded_cards(self.turn)
      replace = self.players[self.turn].get_replacements(unneeded)
      while len(replace) > 0:
        for card in replace:
          self.hands[self.turn].remove(card)
          self.hands[self.turn].append(self.deck.draw())
        unneeded = self.check_unneeded_cards(self.turn)
        replace = self.players[self.turn].get_replacements(unneeded)
      position, card = self.players[self.turn].get_move(self.board, self.last_move, self.hands[self.turn])
      self.hands[self.turn].remove(card)
      if position == None or not self.make_move(position):
        raise Exception('Invalid move')
      self.check_winner(position)
      if self.switch_turn:
        self.change_turn()
      self.render()
    print('Game over!')
    print('Winner is player {}'.format(self.get_winner()))

seq = Sequence()
seq.play()

# TEST LOGIC BELOW 
class SequenceTest:
  def check_winner():
    def make_moves(sequence, moves, switch_turn=True):
      random.shuffle(moves)
      for move in moves:
        sequence.make_move(move)
        sequence.check_winner(move)
        if switch_turn:
          sequence.change_turn()
      return sequence

    # Test check_winner
    # Test 1: 5 in a row horizontally
    switch_turn = False
    s1 = Sequence(switch_turn)
    moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    s1 = make_moves(s1, moves, switch_turn)
    assert s1.has_winner() == True

    # Test 2: 5 in a row vertically
    s2 = Sequence(switch_turn)
    moves = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
    s2 = make_moves(s2, moves, switch_turn)
    assert s2.has_winner() == True

    # Test 3: 5 in a row diagonally
    s3 = Sequence(switch_turn)
    moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
    s3 = make_moves(s3, moves, switch_turn)
    assert s3.has_winner() == True

    # Test 4: Multiple 5 in a row
    s4 = Sequence(switch_turn)
    moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9)]
    s4 = make_moves(s4, moves, switch_turn)
    assert s4.has_winner() == True

    # Test 5: 5 in a row with corners
    s5 = Sequence(switch_turn)
    moves = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
    s5 = make_moves(s5, moves, switch_turn)
    assert s5.has_winner() == True

    # Test 6: No 5 in a row
    s6 = Sequence(switch_turn)
    moves = [(1, 1), (3, 2), (2, 3), (4, 4), (5, 5)]
    s6 = make_moves(s6, moves, switch_turn)
    assert s6.has_winner() == False

    # Test 7: 5 in a row but separate players
    switch_turn = True
    s7 = Sequence(switch_turn)
    moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
    s7 = make_moves(s7, moves, switch_turn)
    assert s7.has_winner() == False

    print("All tests passed for check_winner!")

SequenceTest.check_winner()

seq = Sequence()
seq.play()