import random

class RandAgent():

  def __init__(self):
    self.unneeded = []

  def get_replacements(self, unneeded):
    self.unneeded = unneeded
    return unneeded # which cards to replace from your current unneeded cards in hand

  def get_move(self, board, last_move, hand):
    choice = random.choice(hand)
    while choice not in self.unneeded:
      choice = random.choice(hand)
    for r in range(len(board)):
      for c in range(len(board[0])):
        if board[r][c] == choice:
          return (r, c), choice
    return None, choice