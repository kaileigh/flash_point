#!usr/bin/env python

import sys
from itertools import izip

class facing:
  NORTH, EAST, SOUTH, WEST = range(4)
  move = ((-1,0),(0,1),(1,0),(0,-1))

class fire:
  NONE, SMOKE, FIRE = range(3)

class wall:
  def __init__(self, is_door, is_open, damage):
    self.is_door = is_door
    self.is_open = is_open
    self.damage = damage

class poi:
  def __init__(self, revealed, false_alarm):
    self.revealed = revealed
    self.false_alarm = false_alarm

class space:
  def __init__(self, row, col):
    self.row = row
    self.col = col
    self.fire_status = fire.NONE
    self.hotspot = False
    self.hazmat = False
    self.walls = [None, None, None, None]
    self.adj = [None, None, None, None]
    self.graphics = "", ""

class board:
  def __init__(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.rescued = 0
    self.lost = 0
    self.remaining_damage = 24
    self.grid = [[space(i,j) for j in range(cols)] for i in range(rows)]

def split_input_line(string):
  triplet_list = []
  for i in range(0,len(string),3):
    triplet_list.append(string[i:i+3])
  return triplet_list

def parse_walls(space):
  graphics = space.graphics
  walls = [None] * 4
  if(graphics[0][2] == '+'):
    walls[facing.EAST] = wall(True, False, 0)
  elif(graphics[0][2] == '|'):
    walls[facing.EAST] = wall(False, False, 0)
  if(graphics[1][0] == '+'):
    walls[facing.SOUTH] = wall(True, False, 0)
  elif(graphics[1][0] == '-'):
    walls[facing.SOUTH] = wall(False, False, 0)
  return walls

def print_board(board):
  for row in board.grid:
    for space in row:
      sys.stdout.write(space.graphics[0])
    sys.stdout.write('\n')
    for space in row:
      s = list(space.graphics[1])
      sys.stdout.write(space.graphics[1])
    sys.stdout.write('\n')

def is_clear(wall):
  return wall is None or (wall.is_door and wall.is_open)

def set_fire(board, row, col):
  space = board.grid[row][col]
  if space.fire_status == fire.NONE:
    print "smoke in ", space.row, space.col
    space.fire_status = fire.SMOKE
  elif space.fire_status == fire.SMOKE:
    space.fire_status = fire.FIRE
  elif space.fire_status == fire.FIRE:
    for direction, wall in enumerate(space.walls):
      spread_fire(board, space, wall, direction)
  for row in board.grid:
    for s in row:
      if s.fire_status == fire.SMOKE:
        for adj, wall in zip(s.adj, s.walls):
          if adj is not None and adj.fire_status == fire.FIRE and is_clear(wall):
            s.fire_status = fire.FIRE
            print "flashover in ", s.row, s.col
            sync_graphics(s)
  sync_graphics(space)

def sync_graphics(space):
  if space.fire_status == fire.NONE:
    s = list(space.graphics[0])
    s[1] = ' '
    space.graphics = "".join(s), space.graphics[1]
  if space.fire_status == fire.SMOKE:
    s = list(space.graphics[0])
    s[1] = '#'
    space.graphics = "".join(s), space.graphics[1]
  elif space.fire_status == fire.FIRE:
    s = list(space.graphics[0])
    s[1] = '!'
    space.graphics = "".join(s), space.graphics[1]
  if space.walls[facing.EAST] is None:
    a = list(space.graphics[0])
    a[2] = ' '
    b = list(space.graphics[1])
    b[2] = ' '
    space.graphics = "".join(a), "".join(b)
  elif space.walls[facing.EAST].damage == 1:
    a = list(space.graphics[0])
    a[2] = '/'
    b = list(space.graphics[1])
    b[2] = '/'
    space.graphics = "".join(a), "".join(b)
    print space.graphics
  elif space.walls[facing.EAST].damage == 0:
    if space.walls[facing.EAST].is_door:
      if space.walls[facing.EAST].is_open:
        a = list(space.graphics[0])
        a[2] = '-'
        b = list(space.graphics[1])
        b[2] = '|'
        space.graphics = "".join(a), "".join(b)
      else:
        a = list(space.graphics[0])
        a[2] = '+'
        b = list(space.graphics[1])
        b[2] = '|'
        space.graphics = "".join(a), "".join(b)
    else:
        a = list(space.graphics[0])
        a[2] = '|'
        b = list(space.graphics[1])
        b[2] = '|'
        space.graphics = "".join(a), "".join(b)
  if space.walls[facing.SOUTH] is None:
    a = list(space.graphics[1])
    a[0] = ' '
    a[1] = ' '
    a[2] = ' '
    space.graphics = space.graphics[0], "".join(a)
  elif space.walls[facing.SOUTH].damage == 1:
    a = list(space.graphics[1])
    a[0] = '/'
    a[1] = '/'
    a[2] = '/'
    space.graphics = space.graphics[0], "".join(a)
  elif space.walls[facing.SOUTH].damage == 0:
    if space.walls[facing.SOUTH].is_door:
      if space.walls[facing.SOUTH].is_open:
        a = list(space.graphics[1])
        a[0] = '-'
        a[1] = '|'
        a[2] = '-'
        space.graphics = space.graphics[0], "".join(a)
      else:
        a = list(space.graphics[1])
        a[0] = '-'
        a[1] = '+'
        a[2] = '-'
        space.graphics = space.graphics[0], "".join(a)
    else:
      a = list(space.graphics[1])
      a[0] = '-'
      a[1] = '-'
      a[2] = '-'
      space.graphics = space.graphics[0], "".join(a)

def spread_fire(board, space, wall, direction):
  if space.adj[direction] is None:
    print "hit edge at direction ", direction
    return
  if is_clear(wall):
    new_row = space.row + facing.move[direction][0]
    new_col = space.col + facing.move[direction][1]
    print "spreading to ", new_row, new_col
    adj_space = space.adj[direction]
    if adj_space.fire_status == fire.NONE:
      adj_space.fire_status = fire.SMOKE
    elif adj_space.fire_status == fire.SMOKE:
      adj_space.fire_status = fire.FIRE
    elif adj_space.fire_status == fire.FIRE:
      spread_fire(board, adj_space, adj_space.walls[direction], direction)
    sync_graphics(adj_space)
  elif wall.is_door:
    wall = None
  else:
    wall.damage += 1
    if wall.damage == 2:
      wall = None
  sync_graphics(space)

def link_spaces(this_space, other_space, facing):
  ## N -> S, E -> W, S -> N, W -> E
  other_facing = (facing + 2) % 4 
  this_space.adj[facing] = other_space
  other_space.adj[other_facing] = this_space
  this_space.walls[facing] = other_space.walls[other_facing]

def create_board(name, rows, cols):
  f = open(name, 'r')
  input_buf = f.read().split("\n")
  game_board = board(rows, cols)
  input_lines = []
  for input_line in input_buf:
    input_lines.append(split_input_line(input_line))
  for i, line in enumerate(input_lines):
    if i % 2 == 0:
      for j, half_space in enumerate(line):
        game_board.grid[i / 2][j].graphics = half_space, input_lines[i+1][j]
  for i in range(game_board.rows):
    for j in range(game_board.cols):
      this_space = game_board.grid[i][j]
      this_space.walls = parse_walls(this_space)
      if i > 0:
        link_spaces(this_space, game_board.grid[i-1][j], facing.NORTH)
      if j > 0:
        link_spaces(this_space, game_board.grid[i][j-1], facing.WEST)
  print_board(game_board)
  for x in range(3):
    set_fire(game_board, 1, 2)
  print game_board.grid[1][2].graphics
  print_board(game_board)
  return game_board


