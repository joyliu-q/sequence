import tkinter as tk

class Display():
  def __init__(self, fps=30):
    self.frame_delay = 1000 // fps
    self.window = tk.Tk()
    self.window.geometry("800x600")
    self.window.title("Sequence")

    self.numbers = [0, 0, 0]

    self.l1 = tk.Label(text=self.numbers[0], foreground="white", background="black")
    self.l1.pack()
    self.l2 = tk.Label(text=self.numbers[1], foreground="white", background="black")
    self.l2.pack()
    self.l3 = tk.Label(text=self.numbers[2], foreground="white", background="black")
    self.l3.pack()
  
  def inc_nums(self, i, n):
    self.numbers[i] += n
    
  def update(self):
    self.l1.config(text=self.numbers[0])
    self.l2.config(text=self.numbers[1])
    self.l3.config(text=self.numbers[2])
    #self.window.after(self.frame_delay, self.update)

  def start(self):
    self.window.mainloop()