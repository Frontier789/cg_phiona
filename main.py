from model import *
from camera import *

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
        self.i = 0
        pass
 
    def _draw_frame(self):
        self.car.angle += 0.03
        self.i += 1
        # self.cam.position.y = sin(self.i/30)
        
        # self.cam.position.y += 0.3
        self.cam.render(self.car)
        
        glfw.swap_buffers(self.window)
 
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        
        self.car = model()
        self.car.position = vec3(0,0,-5)
        self.cam = camera()
        self.cam.position = vec3(0,5,0)
        self.cam.target = self.car.position
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._draw_frame()
            glfw.poll_events()

test().main()


