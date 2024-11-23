import math

import moderngl
import pygame
import pygame_shaders
import glm
import time

pygame.init()

clock = pygame.time.Clock()

#Create an opengl pygame Surface, this will act as our opengl context.
screen = pygame.display.set_mode((600, 600), pygame.OPENGL | pygame.DOUBLEBUF)

#This is our main display we will do all of our standard pygame rendering on.
display = pygame.Surface((600, 600))

#The shader we are using to communicate with the opengl context (standard pygame drawing functionality does not work on opengl displays)
screen_shader = pygame_shaders.DefaultScreenShader(display) # <- Here we supply our default display, it's this display which will be displayed onto the opengl context via the screen_shader

#create our target surface
target_surface = pygame.Surface((512, 512))
target_surface.blit(pygame.image.load("image.png"), (0,0))

shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "fragments.glsl", target_surface) #<- give it to our shader
start = time.time()
while True:
    #Fill the display with white
    display.fill((255, 100, 255))

    #Standard pygame event stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    #Render a rect onto the display using the standard pygame method for drawing rects.
    pygame.draw.rect(display, (0, 255, 0), (200, 200, 20, 20))
    pygame.draw.rect(display, (255, 255, 0), (300, 200, 20, 20))
    #print( shader._members )

    oSurf = pygame.Surface((512,512))
    oSurf.blit( display, (0,0) )

    tex =  shader.ctx.texture( (512, 512), 4 )
    tex.write( pygame.image.tostring( oSurf, "RGBA") )
    shader.shader["bottom"].value = 1
    tex.use(location=1)

    tex = shader.ctx.texture( (320, 320), 4 )
    tex.write( pygame.image.tostring(pygame.image.load("noise.png"), "RGBA") )
    shader.shader["noise"].value = 2
    tex.use(location=2)

    tex = shader.ctx.texture( (1024, 1024), 4 )
    tex.write( pygame.image.tostring(pygame.image.load("caustic.jpg"), "RGBA") )
    shader.shader["caustic"].value = 3
    tex.use(location=3)

    shader.shader["time"].value = float(time.time() - start)
    #Render the shader onto the surface object
    target_shader = shader.render()

    #Blit the new (shader applied!) surface onto the display
    display.blit(target_shader, (0, 0))

    #Render the contents of "display" (main surface) onto the opengl screen.
    screen_shader.render()

    #Update the opengl context
    pygame.display.flip()
    clock.tick(60)