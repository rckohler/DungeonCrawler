import random
import copy
import pygame
import sys

def runTest(player):
    m = create_maze()
    maze = m[0]
    tiles = m[1]
    player.maze = maze
    player.tiles = tiles
    player.maze[player._col][player._row]=tiles['player']
    player.ai(player)
    print(player.calculateScore())
def create_maze():

    tiles = {'wall': 'X',
             'weal': '+',
             'woe': '-',
             'blank': ' ',
             'player': 'P'}

    # maze config

    config = createRandomMapConfig()
    rows = config[0]
    cols = config[1]
    openSpaces = config[2]
    numWeals = config[3]
    numWoes = config[4]


    maze = createWalls(cols, rows, openSpaces, tiles)
    if not maze == 'invalid':
        maze = fillOtherCrap(numWeals, numWoes, maze, tiles)

    return maze,tiles
def createRandomMapConfig():
    rows = random.randint(4,100)
    cols = random.randint(4,100)
    openSpaces = random.randint(2,rows-1)
    numWeals = int(abs(random.gauss(0,rows*cols*.1)))
    numWoes = int(abs(random.gauss(0,rows*cols*.1)))
    return rows,cols,openSpaces,numWeals,numWoes

def createWalls(cols, rows, openSpaces, tiles):
    if openSpaces < rows:
        maze = []
        i = 2
        if cols % 2 == 0:
            i = 1
        for col in range(cols + i):
            maze.append([])
            for row in range(rows + 2):
                if row == 0:
                    maze[col].append(tiles['wall'])
                if row == rows + 1:
                    maze[col].append(tiles['wall'])
                else:
                    if col % 2 == 0:
                        maze[col].append(tiles['wall'])
                    else:
                        maze[col].append(tiles['blank'])
        for col in range(cols):

            if col % 2 == 0 and col > 0:
                openSpacesThisCol = openSpaces
                while openSpacesThisCol > 0:
                    r = random.randint(1, rows - 1)
                    if maze[col][r] == tiles['wall']:
                        openSpacesThisCol -= 1
                        maze[col][r] = tiles['blank']

    else:
        print("Unacceptable wall parameters")
        return "invalid"
    return maze


def fillOtherCrap(numWeals, numWoes, maze, tiles):
    rows = len(maze[0])
    cols = len(maze)

    if (numWeals + numWoes) > .5 * rows * cols:
        print("Unacceptable maze parameters in fillOtherCrap")
        return 'invalid'
    while numWeals > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['weal']
            numWeals -= 1
    while numWoes > 0:
        c, r = random.randint(0, cols - 1), random.randint(0, rows - 1)
        if maze[c][r] == tiles['blank']:
            maze[c][r] = tiles['woe']
            numWoes -= 1
    return maze


class Player():
    wealPoints = 10
    woePoints = -100
    tiles = []
    maze = []
    debug = True
    def __init__(self,ai):
        self._col = 1
        self._row = 1
        self.weals = 0
        self.woes = 0
        self.moves = 0
        self.score = 0
        self.ai = ai
    def _move(self, dCol, dRow):
        self.moves+=1
        newCol = self._col + dCol
        newRow = self._row + dRow
        destination = self.maze[newCol][newRow]
        if not destination == self.tiles['wall']:
            self.maze[self._col][self._row]=self.tiles['blank']
            self._col = newCol
            self._row = newRow
            self.maze[self._col][self._row]=self.tiles['player']
            self.sayMaze()
            if destination == self.tiles['weal']:
                self.weals+=1
            if destination == self.tiles['woe']:
                self.woes+=1
        else:
            print("move failed")
            self.score-=1000

    def moveUp(self):
        self._move(0, -1)

    def moveDown(self):
        self._move(0, 1)

    def moveRight(self):
        self._move(1, 0)

    def moveLeft(self):
        self._move(-1, 0)

    def sayMaze(self):
        rows = len(self.maze[0])
        cols = len(self.maze)

        for row in range(rows):
            newRow = []
            message = ''
            for col in range(cols):
                newRow.append(self.maze[col][row])
            for c in newRow:
                message += c
                message += ' '
            self.dSay(message)
        self.dSay("")


    def dSay(self,message):
        if self.debug:
            print(message)

    def calculateScore(self):
        score = self.wealPoints*self.weals+self.woePoints*self.woes-self.moves
        return score

# example AI
def basicAI(self):
    movingDown = True
    while not self._col == len(self.maze)-2:
        if not self.maze[self._col+1][self._row] == self.tiles['wall']:
            self.moveRight()
        if not self.maze[self._col][self._row+1]==self.tiles['wall'] and movingDown:
            self.moveDown()
        if self.maze[self._col][self._row+1]==self.tiles['wall']:
            movingDown = False
        if not self.maze[self._col][self._row-1]==self.tiles['wall'] and not movingDown:
            self.moveUp()
        if self.maze[self._col][self._row-1]==self.tiles['wall']:
            movingDown = True
p1 = Player(basicAI)

runTest(p1)
