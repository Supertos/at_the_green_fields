import console
import map
import clock
import pygame as pg

def onkeyDown( ev ):
    global m
    global a
    if ev.key == pg.K_r:
        m = map.Map()
        m.generate(64, 24)
        m.updateConsoleColor(a, 0, 16 )
        #a.write(m.generateString(), 1, 64)
    pass
def onkeyUp( ev ):
    pass



a = console.Console()
a.keyup = onkeyUp
a.keydown = onkeyDown

m = map.Map()
m.generate(64, 8 )
#m.updateConsoleColor( a, 64, 1 )
#a.write(m.generateString(), 2, 0)
a.flip()

d = clock.Clock()

cc = pg.time.Clock()

odd = True
a.setCol( (255,0,0), 2, 2)
logo = """
######  ######      ######  ######    ######  ######  ##    ##
##  ##    ##        ##      ##  ##    ######  ######  ####  ##
######    ##        ##   #  ######    ##      ##      ##  ####
##  ##    ##        ######  ##    ##  ######  ######  ##    ##
"""

a.write( logo, 0, 0 )
a.write( "[^R]e-generate map", 8, 8 )
a.write( "[^S]ingle-player", 9, 8 )
a.write( "[^M]ulty-player", 10, 8 )
a.write( "[^Q]uit", 14, 8 )

while a.update():
    a.write(f"{d} | {int(cc.get_fps())} FPS | Max speed", 0, 64)

    #a.write( logo, 0, 0 )
    #a.write( "[^R]e-generate map", 8, 8 )
    #a.write( "[^S]ingle-player", 9, 8 )
    #a.write( "[^M]ulty-player", 10, 8 )
    a.write( "[^Q]uit", 14, 8 )

    a.flip()