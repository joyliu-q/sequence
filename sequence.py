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
  
  def __init__(self):
    self.board = [[Cell(c) for c in row] for row in Sequence.CARD_POSITIONS]
    self.height = len(self.board)
    self.width = len(self.board[0])
    self.board[0][0].claim(2)
    self.board[-1][0].claim(2)
    self.board[0][-1].claim(2)
    self.board[-1][-1].claim(2)
    self.turn = 0
    self.has_winner = False

  def make_move(self, position):
    row, col = position
    if row < 0 or row >= self.height or col < 0 or col >= self.width:
      return False
    if self.board[row][col].occupied != None:
      return False
    self.board[row][col].claim(self.turn)
    if self.check_winner():
      self.has_winner = True
    self.switch_turn()
    return True

  def check_winner(self, position): # given that the current move is made, is there a winner
    row, col = position
    # Rows
    for i in range(1, 5):
      if row - i < 0:
        break
      occupied = self.board[row - i][col].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
    for i in range(1, 5):
      if row + i >= len(self.board):
        break
      occupied = self.board[row + i][col].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
    # Cols
    for i in range(1, 5):
      if col - i < 0:
        break
      occupied = self.board[row][col - i].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
    for i in range(1, 5):
      if col + i >= len(self.board[0]):
        break
      occupied = self.board[row][col + i].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
    # Diagonals
    for i in range(1, 5):
      if row - i < 0 or col - i < 0:
        break
      occupied = self.board[row - i][col - i].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
    for i in range(1, 5):
      if row + i >= len(self.board) or col + i >= len(self.board[0]):
        break
      occupied = self.board[row - i][col - i].occupied
      if occupied != self.turn and occupied != 2:
        break
      if i == 4:
        self.has_winner = True
        return
  
  def switch_turn(self):
    self.turn = not self.turn

  # TODO: do this
  def render(self):
    pass
  
  # TODO: do this
  def __str__(self):
    out = ''
    for row in self.board:
      out += ' '.join(map(str, row)) + '\n'
    return out

