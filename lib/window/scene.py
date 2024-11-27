# -=-=-=-=-=-=-=-= Supertos Industries ( 2012 - 2024 ) =-=-=-=-=-=-=-=-
# Author: Supertos
#
# Scene class represents game state
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
class Scene:
    def __init__( self, inputManager=None ):
        self.window = None
        self.renderObjects = []
        inputManager.init(self)
        self._inputManager = inputManager

    def quit( self, newScene ):
        pass

    def init( self, window ):
        self.window = window

    def addRenderObject( self, obj ):
        self.renderObjects.append( obj )

    def removeRenderObject( self, obj ):
        self.renderObjects.remove( obj )

    def inputManager(self):
        return self._inputManager

    def render( self, vX, vY, vScale, canvas, tm, random ):
        for el in self.renderObjects:
            el.render( el.x - vX, el.y - vY, vScale, canvas, tm, random )

