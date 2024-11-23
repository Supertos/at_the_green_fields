import random


class Map:
    def __init__(self):
        self.w = 128
        self.h = 48
        self.regions = []
        self.cells = [[None for _ in range(self.h)] for _ in range(self.w)]
        self.celloccupied = {}

    def occupyCell(self, cell, occupier):
        x, y = cell
        self.cells[x][y] = occupier
        self.celloccupied[cell] = occupier

    def addRegion(self, obj):
        self.regions.append(obj)

        for el in obj.cells:
            self.occupyCell( el, len(self.regions) - 1 )

    def randomFreeNeighbor(self, cell):
        frees = []
        x, y = cell
        if x < self.w - 1 and (x+1, y) not in self.celloccupied: frees.append( (x+1, y) )
        if x > 0 and (x-1, y) not in self.celloccupied: frees.append( (x-1, y) )
        if y < self.h - 1 and (x, y+1) not in self.celloccupied: frees.append( (x, y+1) )
        if y > 0 and (x, y-1) not in self.celloccupied: frees.append( (x, y-1) )

        if len(frees) == 0: return None
        return frees[ random.randint(0, len(frees) - 1) ]

    def randomUnobstructedCell(self, region):
        frees = []
        for cell in region.cells:
            if self.randomFreeNeighbor( cell ): frees.append( cell )
        if len(frees) == 0: return None
        return frees[ random.randint(0, len(frees) - 1) ]

    def tryExpandRegion(self, region):
        randcell = self.randomUnobstructedCell( region )
        if not randcell: return False
        randneig = self.randomFreeNeighbor(randcell)


        self.occupyCell( randneig, region.id )
        region.cells.append( randneig )
        return True


    def tryNewRegion(self):
        r = self.regions[ random.randint(0, len(self.regions) - 1) ]
        while not self.randomUnobstructedCell( r ): r = self.regions[ random.randint(0, len(self.regions) - 1) ]

        c = self.randomUnobstructedCell(r)

        return Region( self, self.randomFreeNeighbor(c) )


    def generate(self, count, size):
        obj = Region(self, (int(self.w / 2), int(self.h / 2)))
        for s in range( size ):
            self.tryExpandRegion(obj)
        for i in range(count - 1):
            obj = self.tryNewRegion()
            for s in range( size ):
                if not self.tryExpandRegion(obj):
                    for cell in obj.cells:
                        x, y = cell
                        del self.celloccupied[(x,y)]
                        self.cells[x][y] = None
                    del obj
                    count += 1
                    break
        return True

    def generateString(self):
        s = ""
        for y in range(self.h):
            for x in range(self.w):
                s += (x, y) in self.celloccupied and chr(ord('A') + self.celloccupied[(x, y)]) or " "
            s += "\n"
        return s

    def updateConsoleColor(self, con, x0, y0):
        for x in range( self.w ):
            for y in range( self.h ):
                cell = (x,y)
                if x + x0 >= con.w: continue
                if y + y0 >= con.h: continue
                if cell in self.celloccupied:
                    r = self.regions[self.celloccupied[cell]]
                    con.setCol(r.color, cell[0] + x0, cell[1] + y0)
                else:
                    con.setCol((100,100,255), cell[0] + x0, cell[1] + y0)


class Region:
    def __init__(self, map, cell):
        self.map = map
        self.cells = [cell]
        self.color = ( random.randint(0,255), random.randint(0,255), random.randint(0,255) )
        map.addRegion( self )

        self.id = len(map.regions) - 1




