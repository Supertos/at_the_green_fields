# -=-=-=-=-=-=-=-= Supertos Industries ( 2012 - 2024 ) =-=-=-=-=-=-=-=-
# Author: Supertos
#
# Test
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import lib.window.screen
import lib.window.input
import lib.window.scene
import lib.window.renderobj
import pygame as pg

win = lib.window.screen.Window( (800, 600) )

image = pg.surface.Surface( (800, 600 ) )
image.blit( pg.image.load( "image.png" ), (0,0) )

image = pg.transform.scale( image, (100, 100 ))

inp = lib.window.input.InputManager()
scn = lib.window.scene.Scene( inp )
win.loadScene( scn )

ob = lib.window.renderobj.OpenGLObject( (128,128), (16,16), win, image )
scn.addRenderObject( ob )
while win.update(): pass
