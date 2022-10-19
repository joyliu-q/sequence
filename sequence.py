from cards import Suit, Card, Deck
from utils import ANSIText
import time, os
from agents import *

ansi = ANSIText()

class Cell:
  def __init__(self, card):
    self.card = card
    self.occupied = None # occupied is either None, Green (0), or Red (1), or Both (2)

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

  @staticmethod
  def has_same_owner(cells):
    owners = set()
    for cell in cells:
      if cell.occupied == None:
        return -1
      owners.add(cell.occupied)
    owners = list(owners)
    if 2 in owners and len(owners) == 2:
      owners.remove(2)
      return owners[0]
    elif len(owners) == 1:
      return owners[0]
    return -1

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
    self.switch_turn = switch_turn
    self.reset()
    self.players = [RandAgent(0), RandAgent(1)]
    self.height = len(self.board)
    self.width = len(self.board[0])

  def reset(self, switch_turn=None):
    if switch_turn != None:
      self.switch_turn = switch_turn
    self.board = [[Cell(c) for c in row] for row in Sequence.CARD_POSITIONS]
    self.board[0][0].claim(2)
    self.board[-1][0].claim(2)
    self.board[0][-1].claim(2)
    self.board[-1][-1].claim(2)
    self.turn = 0
    self.fives = [[], []]
    self.last_move = None
    self.deck = Deck(2, jokers=False, shuffle=True)
    self.hands = [[], []]
    for _ in range(7):
      self.hands[0].append(self.deck.draw())
      self.hands[1].append(self.deck.draw())
    
  def get_hand(self, player):
    return self.hands[player]

  def check_valid_move(self, position, card):
    if position == None:
      return 'Invalid move: No position returned'
    if card == None:
      return 'Invalid move: No card returned'
    if card not in self.hands[self.turn]:
      return 'Invalid move: Card not owned'
    row, col = position
    if row < 0 or row >= self.height or col < 0 or col >= self.width:
      return 'Invalid move: Position out of bounds'
    if (row == 0 or row == self.height - 1) and (col == 0 or col == self.width - 1):
      return 'Invalid move: Position in the corner'
    if card.rank != 11 and self.board[row][col].get_card() != card:
      return 'Invalid move: Card does not match intended position'
    if card.is_one_eyed_jack() and not self.board[row][col].is_occupied():
      return 'Invalid move: One-eyed jack used on unoccupied position'
    if (card.rank != 11 or card.is_two_eyed_jack()) and self.board[row][col].is_occupied():
      return 'Invalid move: Position is occupied'
    return ''

  def make_move(self, position, is_remove_jack=False):
    # If winner is already decided, don't allow any more moves
    if self.has_winner():
      return
    # Otherwise, make the move (already checked as valid move)
    row, col = position
    if is_remove_jack:
      self.board[row][col].unclaim()
    else:
      self.board[row][col].claim(self.turn)
    self.last_move = position
  
  def is_five_unique(self, new_five, previous_fives):
    for prev_five in previous_fives:
      overlap = 0
      for cell in prev_five:
        if cell in new_five:
          overlap += 1
      if overlap > 1:
        return False
    return True

  def check_winner(self, position=None): # given that the current move is made, is there a winner
    if position == None:
      return self.check_winner_entire_board()
    row_offset = [(0, x) for x in range(-4, 5)]
    col_offset = [(x, 0) for x in range(-4, 5)]
    diag_offset_1 = [(x, x) for x in range(-4, 5)]
    diag_offset_2 = [(x, -x) for x in range(-4, 5)]
    offsets = [row_offset, col_offset, diag_offset_1, diag_offset_2]
    row, col = position
    for which_offset in offsets:
      acc = 0
      for i, offset in enumerate(which_offset):
        new_pos = (row + offset[0], col + offset[1])
        if new_pos[0] < 0 or new_pos[0] >= self.height or new_pos[1] < 0 or new_pos[1] >= self.width:
          continue
        if self.board[new_pos[0]][new_pos[1]].occupied == self.turn or self.board[new_pos[0]][new_pos[1]].occupied == 2:
          acc += 1
          if acc == 5:
            five = [(new_pos[0] + r, new_pos[1] + c) for r, c in which_offset[i-4:i+1]]
            if self.is_five_unique(five, self.fives[self.turn]):
              self.fives[self.turn].append(five)
              break
        else:
          acc = 0
    return self.has_winner()

  def check_winner_entire_board(self):
    fives = [[], []]
    row_offset = [(0, x) for x in range(5)]
    col_offset = [(x, 0) for x in range(5)]
    diag_offset_1 = [(x, x) for x in range(5)]
    diag_offset_2 = [(x, -x) for x in range(5)]
    offsets = [(row_offset, (0, self.height), (0, self.width - 4)), (col_offset, (0, self.height - 4), (0, self.width)), (diag_offset_1, (0, self.height - 4), (0, self.width - 4)), (diag_offset_2, (0, self.height - 4), (4, self.width))]
    for o in offsets:
      for r in range(o[1][0], o[1][1]):
        for c in range(o[2][0], o[2][1]):
          five = [(r + offset[0], c + offset[1]) for offset in o[0]]
          owner = Cell.has_same_owner([self.board[y][x] for y, x in five])
          if owner != -1 and owner != 2:
            if self.is_five_unique(five, fives[owner]):
              fives[owner].append(five)
    self.fives = fives
    return self.has_winner()
  
  # State retrieval functions
  def has_winner(self):
    return self.get_winner() != None

  def get_winner(self):
    if len(self.fives[0]) >= 2:
      return 0
    elif len(self.fives[1]) >= 2:
      return 1
    elif self.is_tie():
      return -1
    else:
      return None

  def is_tie(self):
    has_remove = False
    for card in self.hands[1 - self.turn]:
      if card.is_one_eyed_jack():
        has_remove = True
    return not has_remove and self.is_full()

  def is_full(self):
    return self.count_occupied() == self.height * self.width

  def count_occupied(self, card=None):
    count = 0
    for row in self.board:
      for cell in row:
        if cell.is_occupied() and (card == None or cell.card == card):
          count += 1
    return count

  def check_unneeded_cards(self, player):
    return [card for card in self.hands[player] if self.count_occupied(card) >= 2]

  def change_turn(self):
    self.turn = int(not self.turn)

  def render(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(str(self), end='\r')
    #time.sleep(0.1)
  
  def __str__(self):
    out = "Turn:  " + (ansi.green(self.turn) if self.turn == 0 else ansi.red(self.turn))
    out += "  Last move:  " + (ansi.green(self.last_move) if self.turn == 0 else ansi.red(self.last_move)) + '\n'
    for row in self.board:
      out += ' '.join(map(str, row)) + '\n'
    return out

  def play(self):
    # TODO: Fix check for win if the two fives overlap
    # TODO: Add tie state if board is filled and neither (or next?) player has one-eyed jack
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
      is_valid_msg = self.check_valid_move(position, card)
      if is_valid_msg != '':
        raise Exception(is_valid_msg)
      self.make_move(position, is_remove_jack=card.is_one_eyed_jack())
      self.hands[self.turn].remove(card)
      self.hands[self.turn].append(self.deck.draw())
      self.check_winner(position)
      self.render()
      if self.switch_turn:
        self.change_turn()
    print('Game over!')
    w = self.get_winner()
    if w == -1:
      print('Tie game!')
    else:
      print('Winner is player {}'.format(ansi.red(w) if w == 1 else ansi.green(w)))
    return w
