import random

class RandAgent():
  def __init__(self):
    pass

  def get_replacements(self, unneeded):
    return unneeded # which cards to replace from your current unneeded cards in hand

  def get_move(self, board, last_move, hand):
    return random.choice(hand)