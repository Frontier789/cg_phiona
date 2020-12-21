from car import car

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import math
from PIL import Image
from glm import *
from time import time

class test:
    def __init__(self):
        self.car = None
        self.i   = 0
 
    # draw frame
    def _draw_frame(self):
        self.i += 1
        
        # create modelview matrix
        model_view = translate(mat4(), vec3(0,0,-5)) * rotate(mat4(), self.i/30.0, vec3(0,1,0))
 
        # create projection matrix
        proj = perspective(radians(60.0), 1024 / 768, 1, 100)
        
        self.car.render(model_view, proj)
 
        # swap buffers
        glfw.swap_buffers(self.window)
 
    # setup and run OpenGL
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        
        self.car = car()
        
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            self._draw_frame()
            glfw.poll_events()

# run an instance of car
test().main()


