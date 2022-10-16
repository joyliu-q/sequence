import random

class RandAgent():

  def __init__(self):
    self.unneeded = []

  def get_replacements(self, unneeded):
    self.unneeded = unneeded
    return unneeded # which cards to replace from your current unneeded cards in hand

  def get_move(self, board, last_move, hand):
    # TODO Jacks are broken cus we didn't implement that
    choice = random.choice(hand)
    while choice in self.unneeded:
      choice = random.choice(hand)
    print(choice)
    for r in range(len(board)):
      for c in range(len(board[0])):
        if not board[r][c].is_occupied() and board[r][c].get_card() == choice:
          return (r, c), choice
    return None, choice