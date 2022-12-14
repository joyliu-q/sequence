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

  def is_one_eyed_jack(self): # One eyed jack = hearts and spades
    return self.rank == 11 and (self.suit == Suit.HEART or self.suit == Suit.SPADE)

  def is_two_eyed_jack(self): # Two eyed jack = clubs and diamonds
    return self.rank == 11 and (self.suit == Suit.CLUB or self.suit == Suit.DIAMOND)

  def __str__(self):
    out = self.get_rank_str()
    if self.suit == Suit.SPADE:
      return out + 's'
    elif self.suit == Suit.HEART:
      return out + 'h'
    elif self.suit == Suit.CLUB:
      return out + 'c'
    elif self.suit == Suit.DIAMOND:
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
    self.stacks = stacks
    self.jokers = jokers
    self.shuffle_deck = shuffle
    self.count = stacks * (54 if jokers else 52)
    for _ in range(stacks):
      for i in range(1, 14):
        for suit in Suit:
          self.deck.append(Card(i, suit))
      if jokers:
        self.deck.append(Card(0, Suit.SPADE))
        self.deck.append(Card(0, Suit.SPADE))
    if shuffle:
      self.shuffle()
  
  def num_cards_remaining(self):
    return self.count

  def is_empty(self):
    return self.count == 0
  
  def draw(self):
    if self.is_empty():
      new_deck = Deck(stacks=self.stacks, jokers=self.jokers, shuffle=self.shuffle_deck)
      self.deck = new_deck.deck
      self.count = new_deck.count
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