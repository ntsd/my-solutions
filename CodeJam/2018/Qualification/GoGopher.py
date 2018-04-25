import sys

def goGopher(a):
  win = False
  if a == 20:
      rows, cols = 4, 5
  else:
      rows, cols = 10, 20
  print(rows, cols,file=sys.stderr)
  trees = [[False for x in range(cols)] for y in range(rows)]
  for y, row in enumerate(trees):
      if win:
          break
      for x, tree in enumerate(row):
          if win:
              break
          while tree is False:
              print(max(2, min(rows - 1, y + 2)), max(2, min(cols - 1, x + 2)))
              sys.stdout.flush()
              i, j = map(int, input().split(' '))
              if i == -1 and j == -1:
                  sys.exit(-1)
              if i == 0 and j == 0:
                  win = True
                  break
              trees[i - 1][j - 1] = True
              tree = trees[y][x]
      print(trees,file=sys.stderr)

for _ in range(int(input())):
  a=int(input())
  goGopher(a)
