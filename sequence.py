from enum import Enum

class Suit(Enum):
  SPADE = 1
  HEART = 2
  CLUB = 3
  DIAMOND = 4

# Sequence board game
class Card:
  def __init__(self, rank=1, suit=Suit.SPADE):
    self.rank = rank # 0 = joker, 1 = ace, 2 = 2, ..., 10 = 10, 11 = jack, 12 = queen, 13 = king
    self.suit = suit # 1 = spades, 2 = hearts, 3 = clubs, 4 = diamonds

  def __str__(self):
      return self.rank + " of " + self.suit

class Deck:
  def __init__(self, stacks=1):
    self.deck = []

class Sequence:
  def __init__(self):
    self.board = [
      [Card(0, Suit.SPADE), Card(2, Suit.SPADE), Card(3, Suit.SPADE), Card(4, Suit.SPADE), Card(5, Suit.SPADE), Card(6, Suit.SPADE), Card(7, Suit.SPADE), Card(8, Suit.SPADE), Card(9, Suit.SPADE), Card(0, Suit.SPADE)],
      [Card(6, Suit.CLUB), Card(5, Suit.CLUB), Card(4, Suit.CLUB), Card(3, Suit.CLUB), Card(2, Suit.CLUB), Card(1, Suit.HEART), Card(13, Suit.HEART), Card(12, Suit.HEART), Card(10, Suit.HEART), Card(10, Suit.SPADE)],
      [Card(7, Suit.CLUB), '1s', '2d', '3d', '4d', '5d', '6d', '7d', '9h', 'Qs'],
      ['8c', 'Ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'Ks'],
      ['9c', 'Qs', '7c', '6h', '5h', '4h', '1h', '9d', '7h', '1s'],
      ['Tc', 'Ts', '8c', '7h', '2h', '3h', 'Kh', 'Td', '8h', 'Ks'],
      ['8c', 'Ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'Ks'],
      ['8c', 'Ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'Ks'],
      ['8c', 'Ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'Ks'],
      ['8c', 'Ks', '6c', '5c', '4c', '3c', '2c', '8d', '8h', 'Ks']
    ]

  def render(self):
    return
  
  def __str__(self):
    
