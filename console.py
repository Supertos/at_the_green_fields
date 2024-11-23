import random
import time

import clock
import map
import pygame as pg

class Console:
    def __init__(self):
        self.w = 128
        self.h = 64

        self.keyup = None
        self.keydown = None

        pg.font.init()

        self.updlines = {}

        self.font = pg.font.SysFont( "Consolas", 16, False, False )
        self.cw, self.ch = self.font.size("1")

        pg.display.init()
        self.win = pg.display.set_mode( ( self.w * self.cw, self.h * self.ch ) )
        self.lines = [ "" for _ in range( self.h ) ]
        self.colors = [[(0,0,0) for _ in range(self.h)] for _ in range( self.w )]

        self.win.fill((0, 255, 0))

    def flip(self):

        for line in range(0, len(self.lines)):
            if line in self.updlines:
                self.colorizeLine(line)
                self.win.blit( self.font.render( self.lines[line], True, (200, 200, 200) ), (0,line * self.ch) )

        pg.display.flip()

        self.updlines = {}

    def setCol(self, col, x, y):
        self.updlines[y] = True
        self.colors[x][y] = col

    def colorizeLine(self, line):
        start = 0
        end = 0

        while start < self.w:
            col = self.colors[start][line]
            while end < self.w and self.colors[end ][line] == col:
                end += 1

            r = pg.rect.Rect( (start * self.cw, line * self.ch), ((end - start) * self.cw, self.ch) )
            self.win.fill(col, r)

            start = end

    def update(self):
        while pg.event.peek():
            a = pg.event.poll()
            if a.type == pg.QUIT:
                return False
            elif a.type == pg.KEYDOWN:
                self.keydown( a )
            elif a.type == pg.KEYUP:
                self.keyup( a )
        return True

    def appendChar(self, char, line, pos):
        if line >= self.h: return
        self.updlines[ line ] = True

        if pos < len(self.lines[line]):
            self.lines[line] = self.lines[line][:pos] + char + self.lines[line][pos + 1:]
        elif pos == len( self.lines[line] ):
            self.lines[line] += char
        else:
            while len( self.lines[line] ) != pos:
                self.lines[line] += " "
            self.lines[line] += char

    def write(self, txt, line, pos=-1):
        writeOffset = pos

        if pos == -1:
            pos = len(self.lines[line])
            writeOffset = 0

        for char in txt:
            if char == "\b":
                pos -= 1
            elif char == "\n":
                line += 1
                pos = writeOffset
            else:
                self.appendChar( char, line, pos )
                pos += 1
