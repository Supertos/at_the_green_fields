# -=-=-=-=-=-=-=-= Supertos Industries ( 2012 - 2024 ) =-=-=-=-=-=-=-=-
# Author: Supertos
#
# Pygame screen class
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import random
import time

import moderngl
import pygame as pg

from lib.window import renderobj
from lib.window.scene import Scene
class Window:
    def __init__( self, size, inputManager=None, icon=None, name=None ):
        if not pg.display.get_init(): pg.display.init()

        self._canvas = pg.display.set_mode( size, pg.OPENGL | pg.DOUBLEBUF )
        if icon: pg.display.set_icon( pg.image.load(icon) )
        if name: pg.display.set_caption( name )

        self._canvasW, self._canvasH = size
        self._caption = name
        self._icon = icon

        self._scene = None

        self._virtualX = 0
        self._virtualY = 0

        self._virtualScale = 1

        self._clock = pg.time.Clock()
        self._fps = 0

        self._context = moderngl.create_context()
        self._context.enable( moderngl.BLEND )
        self._context.blend_func = self._context.SRC_ALPHA, self._context.ONE_MINUS_SRC_ALPHA

        self._begin = float(time.time())

    def context(self):
        return self._context

    def canvas( self ):
        return self._canvas

    def width( self ):
        return self._canvasW

    def height( self ):
        return self._canvasH

    def size( self ):
        return self.width(), self.height()

    def loadScene( self, scene:Scene ):
        if self._scene: self._scene.quit( scene )

        self._scene = scene
        self._scene.init( self )

    def fps( self ):
        return self._fps

    def renderScene( self ):
        tm = self._begin - float(time.time())
        if not self._scene: AssertionError("renderScene error: No scene to render!")

        cnv = pg.surface.Surface( (self._canvasW, self._canvasH) )
        cnv.fill((100, 0, 0))

        self._scene.render( self._virtualX, self._virtualY, self._virtualScale, cnv, tm, random.random() )

        ob = renderobj.OpenGLObject( (self._canvasW, self._canvasH), (0,0), self, cnv )
        ob.renderGLDirect()
        ob.free()

        print( self._fps )

        pg.display.flip()
        self._clock.tick(60)
        self._fps = self._clock.get_fps()

    def update( self ):
        while pg.event.peek():
            if not self._scene.inputManager().onEvent( pg.event.poll() ): return False

        self.renderScene()
        return True