
import re
import sys

from ..utils.io import readlines
from functools import reduce

class Dir:
  def __init__(self, name, parent):
    self.name = name
    self.parent = parent or self
    self.child_dirs = {}
    self.child_files = {}

  def child_dir(self, cname):
    return self.child_dirs.setdefault(cname, Dir(cname, self))

  def child_file(self, size, name):
    self.child_files[name] = int(size)

  def compute_size(self):
    for cd in self.child_dirs.values():
      cd.compute_size()

    self.size = sum(self.child_files.values()) + sum([cd.size for cd in self.child_dirs.values()])

class State:
  def __init__(self, cmd):
    self.root = Dir('/', None)
    self.cwd = self.root
    self.cmd = cmd

  def find_small_dirs(self):
    self.root.compute_size()

    dirs = [self.root]
    smalls = []

    while len(dirs) > 0:
      d = dirs.pop(0)
      dirs.extend(d.child_dirs.values())

      if d.size <= 100000:
        smalls.append(d)
  
    return smalls

  def find_update_space(self):
    total_space  = 70000000
    update_space = 30000000

    used_space = self.root.size
    free_space = total_space - used_space
 
    needed_space = update_space - free_space

    deldir = self.root
    dirs = list(self.root.child_dirs.values())

    while len(dirs) > 0:
      d = dirs.pop(0)
      dirs.extend(d.child_dirs.values())
      if d.size > needed_space and d.size < deldir.size:
        deldir = d

    return deldir
    

def process_cd(state, output=None):
  if state.cmd[1] == '/':
    state.cwd = state.root
  elif state.cmd[1] == '..':
    state.cwd = state.cwd.parent
  else:
    state.cwd = state.cwd.child_dir(state.cmd[1])

  return state

def process_ls(state, output=None):
  if output is None:
    return state
  elif output[0] == 'dir':
    state.cwd.child_dir(output[1])
  else:
    state.cwd.child_file(*output)

  return state

commands = {
  'cd': process_cd,
  'ls': process_ls,
}

def processCmd(state, line):
  parsed = line[:-1].split(' ')
  out = None
  if parsed[0] == '$':
    state.cmd = parsed[1:]
  else:
    out = parsed
  state = commands[state.cmd[0]](state, out)

  return state

state = readlines(sys.argv[1], processCmd, State('$ nop'.split(' ')))

small_dirs = state.find_small_dirs()
print(sum([sd.size for sd in small_dirs]))

print(state.find_update_space().size)

