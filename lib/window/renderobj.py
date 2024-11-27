# -=-=-=-=-=-=-=-= Supertos Industries ( 2012 - 2024 ) =-=-=-=-=-=-=-=-
# Author: Supertos
#
# Render objects get rendered on the screen! Yaaay!
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import moderngl
import pygame as pg
import numpy as np
import array

class RenderObject:
    def __init__( self, size, pos, window ):
        self.x, self.y = pos
        self.w, self.h = size

    def render( self, x, y, scale, canvas, tm, random ):
        pass


class OpenGLObject(RenderObject):
    DEFAULT_VERTEX_SHADER = """
    #version 330 core
    
    in vec2 vPos;
    in vec2 vTex;
    out vec2 uvs;
    
    void main() {
        uvs = vTex;
        gl_Position = vec4(vPos, 0.0, 1.0);
    }
    """

    DEFAULT_FRAGMENT_SHADER = """
    #version 330 core
    
    uniform sampler2D tex;
    uniform float time;
    uniform float random;
    
    in vec2 uvs;
    out vec4 f_color;
    
    void main() {
        vec2 sample_pos = vec2(uvs.x, uvs.y);
        f_color = vec4(texture(tex, sample_pos).rg + sin(time), texture(tex, sample_pos).b, 1.0);
    }
    """

    def __init__( self, size, pos, window, baseSurf, fragmentPath=None, vertexPath=None ):
        super().__init__( size, pos, window )

        self._size = size
        self._out = None

        fragmentCode = OpenGLObject.DEFAULT_FRAGMENT_SHADER
        vertexCode = OpenGLObject.DEFAULT_VERTEX_SHADER

        if fragmentPath:
            with open( fragmentPath, "r" ) as f: fragmentCode = f.read()

        if vertexPath:
            with open( vertexPath, "r" ) as f: vertexCode = f.read()

        self._shader = window.context().program(vertex_shader=vertexCode, fragment_shader=fragmentCode)

        self.inputBuffer = window.context().buffer(data=array.array( 'f',
        [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0
        ]))

        self.vao = window.context().vertex_array( self._shader, [
            ( self.inputBuffer, "2f 2f", "vPos", "vTex")
        ])

        self._baseSurf = baseSurf

        self._texture = window.context().texture( baseSurf.get_size(), 4 )
        self._texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self._texture.swizzle = isinstance(baseSurf, pg.surface.Surface) and "BGRA" or "RGBA"
        self._texture.write( baseSurf.get_view('1') )

        self.textureCount = 1

        self._frameBuffer = window.context().simple_framebuffer(size=self._baseSurf.get_size(), components=4)
        self._scope = window.context().scope(self._frameBuffer)

        self._uniforms = {}
        self._textures = {}


    def addUniform(self, name, obj):
        self._uniforms[name] = obj
        self.updateUniform( name, obj )

    def updateUniform(self, key, val):
        self._textures[key] = self._shader.ctx.texture( val.get_size(), 4 )
        self._textures[key].filter = (moderngl.NEAREST, moderngl.NEAREST)
        self._textures[key].swizzle = isinstance(val, pg.surface.Surface) and "BGRA" or "RGBA"
        self._textures[key].write( val.get_view('1') )

    @staticmethod
    def isTexture(obj):
        return isinstance(obj, pg.surface.Surface) or isinstance(obj, pg.image.Image)

    def updateUniforms(self):
        for key, val in enumerate(self._uniforms):
            if OpenGLObject.isTexture(val) and key not in self._textures:
                self.updateUniform( key, val )

    def uploadUniforms(self):
        usage = self.textureCount
        for key, val in enumerate(self._uniforms):
            if OpenGLObject.isTexture(val):
                self._shader[key] = usage
                self._textures[key].use(usage)
                usage += 1
            else:
                self._shader[key] = val

    def renderGL(self, time, random):
        self._texture.use(0)
        self._shader["tex"] = 0
        if "time" in self._shader: self._shader["time"] = time
        if "random" in self._shader: self._shader["random"] = random
        self.uploadUniforms()
        with self._scope:
            self._frameBuffer.use()
            self.vao.render( mode=moderngl.TRIANGLE_STRIP )
            self._out = pg.image.frombuffer(self._frameBuffer.read(), self._baseSurf.get_size(), "RGB")

    def renderGLDirect(self, time=0, random=0):
        self._texture.use(0)
        self._shader["tex"] = 0
        if "time" in self._shader: self._shader["time"] = time
        if "random" in self._shader: self._shader["random"] = random

        self.vao.render( mode=moderngl.TRIANGLE_STRIP )

    def render( self, x, y, scale, canvas, time=0, random=0 ):
        self.renderGL(time, random)
        canvas.blit( self._out, (x,y) )

    def free(self):
        self._texture.release()
        self._scope.release()

        for el in self._textures:
            el.release()
