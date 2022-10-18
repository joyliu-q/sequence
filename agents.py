from cards import Suit, Card, Deck
import random

class RandAgent():

  def __init__(self):
    self.unneeded = []

  def get_replacements(self, unneeded):
    self.unneeded = unneeded
    return unneeded # which cards to replace from your current unneeded cards in hand

  def get_move(self, board, last_move, hand, agent_turn):
    choice = random.choice(hand)
    while choice in self.unneeded:
      choice = random.choice(hand)
    valid_positions = []
    for r in range(len(board)):
      for c in range(len(board[r])):
        if (r != 0 and r != len(board) - 1) or (c != 0 and c != len(board[r]) - 1):
          if choice.rank != 11:
            if not board[r][c].is_occupied() and board[r][c].get_card() == choice:
              valid_positions.append((r, c))
          elif choice.is_one_eyed_jack(): # one-eyed jack
            if board[r][c].is_occupied() and board[r][c].occupied != agent_turn:
              valid_positions.append((r, c))
          elif choice.is_two_eyed_jack(): # two-eyed jack
            if not board[r][c].is_occupied():
              valid_positions.append((r, c))
    return random.choice(valid_positions), choice
