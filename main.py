from sequence import *
from tests import SequenceTest
from display import *

test = SequenceTest()
test.check_winner()

seq = Sequence()
w = seq.play(render=True, delay=0)
print('Game Over!')
if w == -1:
  print('Tie game!')
else:
  print('Winner is player {}'.format(ansi.red(w) if w == 1 else ansi.green(w)))

#window = Display(fps=1)

def play_games(n, render=True):
  seq = Sequence()
  counts = [0, 0, 0]
  for i in range(n):
    w = seq.play(render=render)
    counts[w] += 1
    seq.reset()
    if i % 50 == 0:
      print(i)
  return counts

def start_display():
  window.update()
  window.start()

#start_display()
counts = play_games(200, render=False)
print(counts)