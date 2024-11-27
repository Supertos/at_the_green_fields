# -=-=-=-=-=-=-=-= Supertos Industries ( 2012 - 2024 ) =-=-=-=-=-=-=-=-
# Author: Supertos
#
# Input Manager reacts on events
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import pygame as pg
class InputManager:
    def __init__( self ):
        pass

    def init( self, scene ):
        pass

    def onEvent( self, event ):
        if event.type == pg.QUIT: return False
        return True