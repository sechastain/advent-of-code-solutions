
import sys
import itertools

bingo_input = [x.strip() for x in open(sys.argv[1], 'r').readlines()]

called_numbers = bingo_input[0].split(",")

board_offset = 2

boards = []

while board_offset < len(bingo_input):
  board = bingo_input[board_offset:board_offset+5]
  board = [list(itertools.filterfalse(lambda x: x == '', b.split(' '))) for b in board]
  
  boards.append(board)
  board_offset += 6

board_marks = {}

def initialize_marks():
  for board_id in range(len(boards)):
    board_marks[board_id] = {"rows":{}, "cols": {}}
initialize_marks()

def mark_board(board_id, anum):
  board = boards[board_id]
  marks = board_marks[board_id]
  for row in range(len(board)):
    col = board[row].index(anum) if anum in board[row] else -1
    if col >= 0:
      marks["rows"][row] = rowscore = marks["rows"].get(row, 0) + 1
      marks["cols"][col] = colscore = marks["cols"].get(col, 0) + 1
      if 5 in [rowscore, colscore]:
        return board_id
  return None
      

def call_number(anum):
  for board_id in range(len(boards)):
    if mark_board(board_id, anum) is not None:
      return board_id
  return None

def score_board(nums, board_id):
  board = list(itertools.chain.from_iterable(boards[board_id]))
  marked_sum = sum([int(x) for x in board if x in nums])
  unmarked_sum = sum([int(x) for x in board if x not in nums])

  print(nums)
  print(boards[board_id])
  print(marked_sum)
  print(unmarked_sum)
  print(int(nums[-1]) * unmarked_sum)
  

for num_id in range(len(called_numbers)):
  board_id = call_number(called_numbers[num_id])
  if board_id is not None:
    score_board(called_numbers[:num_id+1], board_id)
    break


