class ANSIText:
  def __init__(self):
    pass

  def red(self, skk): return "\033[91m {}\033[00m" .format(skk)
 
  def green(self, skk): return "\033[92m {}\033[00m" .format(skk)
  
  def yellow(self, skk): return "\033[93m {}\033[00m" .format(skk)
  
  def lightPurple(self, skk): return "\033[94m {}\033[00m" .format(skk)

  def purple(self, skk): return "\033[95m {}\033[00m" .format(skk)

  def cyan(self, skk): return "\033[96m {}\033[00m" .format(skk)
  
  def lightGray(self, skk): return "\033[97m {}\033[00m" .format(skk)

  def black(self, skk): return "\033[98m {}\033[00m" .format(skk)