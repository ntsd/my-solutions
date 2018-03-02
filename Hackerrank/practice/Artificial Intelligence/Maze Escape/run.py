# /usr/bin/env python
# coding=utf-8
from __future__ import print_function

import json
import os.path
import shutil
import subprocess
import sys
from argparse import ArgumentParser, FileType
from contextlib import contextmanager, closing
from functools import partial
from tempfile import mkdtemp
from textwrap import dedent

BASE_PATH = partial(os.path.join, os.path.abspath(os.path.dirname(__file__)))

# DEFAULTS
TARGET = BASE_PATH('main.py')
MOVES = BASE_PATH('moves.json')
MAX_MOVES = 50
EXECUTABLE = sys.executable


class Board(object):
    _state = []
    op = {
        'LEFT': lambda y, x: (y, x - 1),
        'RIGHT': lambda y, x: (y, x + 1),
        'UP': lambda y, x: (y - 1, x),
        'DOWN': lambda y, x: (y + 1, x),
    }

    def __init__(self, state):
        self.state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = [[char for char in row] for row in value.split('\n') if row]

    def __iter__(self):
        """Iterate cells in state"""

        return ((y, x, char) for y, row in enumerate(self.state) for x, char in enumerate(row))

    def find(self, target='b'):
        """Find cell coord by character"""

        for (y, x, char) in self:
            if char == target:
                return y, x

        raise InvalidTarget()

    def set(self, y, x, value):
        """Set cell in state to value"""

        target = self.state[y][x]

        if target == '#':
            raise InvalidTarget('Cannot cross #')

        self.state[y][x] = value

        if target == 'e':
            raise GameWon()

    def move(self, direction):
        """Move bot in direction"""

        direction = direction.strip()
        if direction not in self.op.keys():
            raise InvalidTarget('Direction not in UP LEFT RIGHT DOWN')

        # rotate state
        self.state = self.rotate(str(self), direction)

        # move bot
        pos_y, pos_x = self.find()  # get bot pos
        next_y, next_x = self.op['UP'](pos_y, pos_x)  # get next bot pos

        self.set(pos_y, pos_x, '-')  # remove bot
        self.set(next_y, next_x, 'b')  # set bot

    def view(self):
        """Get bot's POV"""

        pos_y, pos_x = self.find()  # bot position

        data = [
            [self.state[pos_y - 1][pos_x - 1], self.state[pos_y - 1][pos_x + 0], self.state[pos_y - 1][pos_x + 1]],
            [self.state[pos_y - 0][pos_x - 1], '-', self.state[pos_y - 0][pos_x + 1]],
            [self.state[pos_y + 1][pos_x - 1], self.state[pos_y + 1][pos_x + 0], self.state[pos_y + 1][pos_x + 1]],
        ]
        return self.to_string(data)

    def __str__(self):
        return self.to_string(self.state)

    @staticmethod
    def rotate(state, direction):
        """Rotate grid in direction"""

        state = [list(line) for line in state.split('\n')]  # state as list of lists
        next_state = None

        # rotate cells in state
        if direction == 'UP':
            next_state = state
        if direction == 'RIGHT':
            next_state = reversed(list(zip(*state)))
        if direction == 'DOWN':
            next_state = [reversed(args) for args in reversed(state)]
        if direction == 'LEFT':
            next_state = [reversed(args) for args in zip(*state)]

        if next_state is None:
            raise InvalidTarget('Direction not in UP RIGHT DOWN LEFT')

        # return state as string
        return Board.to_string(next_state)

    @staticmethod
    def to_string(state):
        return '\n'.join(''.join(row) for row in state)


class InvalidTarget(Exception):
    pass


class GameWon(Exception):
    pass


@contextmanager
def temp_dir(copy_targets=None):
    """Create temp directory context"""

    copy_targets = copy_targets or []

    # create temp directory
    path = mkdtemp()
    tmpdir = partial(os.path.join, path)

    # copy each target into temp directory
    for target in copy_targets:
        filename = os.path.basename(target)
        shutil.copy(target, tmpdir(filename))

    # cd temp directory
    os.chdir(tmpdir())

    # yield context handle
    yield tmpdir

    # remove temp directory
    shutil.rmtree(tmpdir())


@contextmanager
def process(command, **kwargs):
    """Create subprocess context"""

    kwargs.setdefault('stdin', subprocess.PIPE)
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    kwargs.setdefault('universal_newlines', True)

    # create subprocess
    handle = subprocess.Popen(command, **kwargs)

    # yield context handle
    yield handle


def run(command, stdin):
    """Call a command in a subprocess"""

    # create subprocess context
    with process(command) as p:
        # send input, collect output
        stdout, stderr = p.communicate(input=stdin)

    return stdin, stdout.rstrip(), stderr.rstrip()


def create_parser():
    """Create an argument parser"""

    parser = ArgumentParser(description='Run maze escape.')
    parser.add_argument('-e', '-p', '--exec', default=EXECUTABLE, dest='executable',
                        help='Executable to run code (%s)' % os.path.basename(EXECUTABLE))
    parser.add_argument('-f', '--file', default=TARGET, dest='target',
                        help='File for executable to call (%s)' % os.path.basename(TARGET))
    parser.add_argument('-o', '--out', default=MOVES, dest='moves', type=FileType('w'),
                        help='File to dump moves (%s)' % os.path.basename(MOVES))
    parser.add_argument('-m', '--max', default=MAX_MOVES, type=int, dest='max_moves',
                        help='Max number of moves (%d)' % MAX_MOVES)

    return parser.parse_args()


def main():
    args = create_parser()

    # create initial board
    board = Board(dedent("""
        #######
        #--#--#
        #--#b-#
        #--#--#
        e-----#
        #-----#
        #######
    """)[1:-1])

    # collect moves
    moves = []

    with temp_dir(copy_targets=[args.target]) as tmpdir:
        command = args.executable, tmpdir(args.target)  # ("python", "main.py")

        for move in range(args.max_moves):
            # run command
            stdin, stdout, stderr = run(command, '1\n%s' % board.view())

            try:
                # update boards state
                board.move(stdout)
            except GameWon:
                break
            except InvalidTarget as e:
                print(e)
                break
            finally:
                # print details about move
                print()
                if stderr:
                    print('STDERR')
                    print(stderr)
                print('STDIN    STDOUT', stdout)
                print(stdin)

                # collect details about move
                moves.append({
                    'move': move,
                    'stdin': stdin,
                    'stdout': stdout,
                    'stderr': stderr,
                })

    # dump details about move to file
    with closing(args.moves) as f:
        json.dump(moves, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
