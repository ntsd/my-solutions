import random


class GuessGame:
  def __init__(self, max_num):
    print("maximum number is %d"%max_num)
    self.max_num = max_num
    self.target = random.randrange(self.max_num) + 1
    self.count = 0
    self.end = False

  def validate(self, num_str):
    if num_str == "exit":
      self.end = True
      return False
    try:
      number = int(num_str)
    except:
      print("you can only input number")
      return False
    if number > self.max_num or number < 1:
      print("number should in range 1-%d" % self.max_num)
      return False
    self.count += 1
    if self.count > 10:
      self.end = True
      print("you have guess more than 10 times")
      return False
    return number

  def guess(self, num_str):
    number = self.validate(num_str)
    if not number:
      return
    if number == self.target:
      print("you guessed")
      self.end = True
      return
    if number > self.target:
      print("the target is lower")
    else:
      print("the target is upper")
    self.end = False
    return

try:
  guess_game = GuessGame(int(input("add maximum number: ")))
except:
  guess_game = GuessGame(int(100))
while not guess_game.end:
  guess_game.guess(input("the number you'll guess or enter exit to exit game: "))
print("you have exit the game")
