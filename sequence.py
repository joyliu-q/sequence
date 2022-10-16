from enum import Enum
import random

class Suit(Enum):
  SPADE = 1
  HEART = 2
  CLUB = 3
  DIAMOND = 4

class Card:
  def __init__(self, rank=1, suit=Suit.SPADE):
    self.rank = rank # 0 = joker, 1 = ace, 2 = 2, ..., 10 = 10, 11 = jack, 12 = queen, 13 = king
    self.suit = suit # 1 = spades, 2 = hearts, 3 = clubs, 4 = diamonds

  def get_rank_str(self):
    if self.rank == 0:
      return 'X'
    elif self.rank == 1:
      return 'A'
    elif self.rank == 10:
      return 'T'
    elif self.rank == 11:
      return 'J'
    elif self.rank == 12:
      return 'Q'
    elif self.rank == 13:
      return 'K'
    else:
      return str(self.rank)

  def __str__(self):
    print(self.suit)
    out = self.get_rank_str()
    if self.suit.value == 1:
      return out + 's'
    elif self.suit.value == 2:
      return out + 'h'
    elif self.suit.value == 3:
      return out + 'c'
    elif self.suit.value == 4:
      return out + 'd'

  def __lt__(self, other):
    if not isinstance(other, self.__class__):
      return False
    if self.suit == other.suit:
      return self.rank < other.rank
    return self.suit < other.suit
  
  def __hash__(self):
    return 14 * self.suit.value + self.rank

  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    return self.rank == other.rank and self.suit == other.suit

  def __ne__(self, other):
    return not self.__eq__(other)

class Deck:
  def __init__(self, stacks=1, jokers=True, shuffle=True):
    self.deck = []
    self.count = stacks * (54 if jokers else 52)
    for _ in range(stacks):
      for i in range(1, 13):
        for suit in Suit:
          self.deck.append(Card(i, suit))
      if jokers:
        self.deck.append(Card(0, Suit.SPADE))
        self.deck.append(Card(0, Suit.SPADE))
    if shuffle:
      self.shuffle()
  
  def num_cards_remaining(self):
    return self.count
  
  def draw(self):
    self.count -= 1
    return self.deck.pop(0)
    
  def shuffle(self):
    random.shuffle(self.deck)
    
  def __eq__(self, other):
    if not isinstance(other, self.__class__):
      return False
    if self.count != other.count:
      return False
    return self.deck == other.deck

  def __ne__(self, other):
    return not self.__eq__(other)

class Cell:
  def __init__(self, card):
    self.card = card
    self.occupied = None # occupied is either None, Green (0), or Blue (1), or Both (2)
  
  def claim(self, player):
    if player != 0 and player != 1 and player != 2:
      return
    self.occupied = player

  def unclaim(self): # If there's a one-eye jack
    self.occupied = None

  def occupied(self):
    return self.occupied
  
  def __str__(self):
    if self.occupied == 0:
      return '00'
    elif self.occupied == 1:
      return '11'
    elif self.occupied == 2:
      return '**'
    else:
      return str(self.card)

class Agent1():
  def __init__(self):
    pass

  def get_move(self):
    pass

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

  def __init__(self, pause_switch_turn=False):
    self.board = [[Cell(c) for c in row] for row in Sequence.CARD_POSITIONS]
    self.height = len(self.board)
    self.width = len(self.board[0])
    self.board[0][0].claim(2)
    self.board[-1][0].claim(2)
    self.board[0][-1].claim(2)
    self.board[-1][-1].claim(2)
    self.players = [Agent1(), Agent1()]
    self.turn = 0
    self.fives = [0, 0] # [Green, Blue]
    self.pause_switch_turn = pause_switch_turn
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
    if self.board[row][col].occupied != None:
      return False
    self.board[row][col].claim(self.turn)
    self.last_move = position
    return True
  
  def has_winner(self):
    return self.fives[0] >= 2 or self.fives[1] >= 2

  def get_winner(self):
    if self.fives[0] >= 2:
      return 0
    elif self.fives[1] >= 2:
      return 1
    else:
      return None

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
  
  def switch_turn(self):
    self.turn = int(not self.turn)

  # TODO: do this
  def render(self):
    pass
  
  def __str__(self):
    out = ''
    for row in self.board:
      out += ' '.join(map(str, row)) + '\n'
    return out

  def play(self):
    while not self.has_winner(self.last_move):
      position = self.players[self.turn].get_move(self.board, self.last_move, self.hands[self.turn])
      if not self.make_move(position):
        raise Exception('Invalid move')
      self.check_winner(position)
      if not self.pause_switch_turn:
        self.switch_turn()
      print(self) # Instead of self.render() temporarily
    print('Game over!')


# TEST LOGIC BELOW 
def make_moves(sequence, moves):
  random.shuffle(moves)
  for move in moves:
    sequence.make_move(move)
    sequence.check_winner(move)
  return sequence

# Test check_winner
# Test 1: 5 in a row horizontally
s1 = Sequence(pause_switch_turn=True)
moves = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
s1 = make_moves(s1, moves)
assert s1.has_winner() == True

# Test 2: 5 in a row vertically
s2 = Sequence(pause_switch_turn=True)
moves = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]
s2 = make_moves(s2, moves)
assert s2.has_winner() == True

# Test 3: 5 in a row diagonally
s3 = Sequence(pause_switch_turn=True)
moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5)]
s3 = make_moves(s3, moves)
assert s3.has_winner() == True

# Test 4: Multiple 5 in a row
s4 = Sequence(pause_switch_turn=True)
moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9)]
s4 = make_moves(s4, moves)
assert s4.has_winner() == True

# Test 5: 5 in a row with corners
s5 = Sequence(pause_switch_turn=True)
moves = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4)]
s5 = make_moves(s5, moves)
assert s5.has_winner() == True

# Test 6: No 5 in a row
s6 = Sequence(pause_switch_turn=True)
moves = [(1, 1), (3, 2), (2, 3), (4, 4), (5, 5)]
s6 = make_moves(s6, moves)
assert s6.has_winner() == False
