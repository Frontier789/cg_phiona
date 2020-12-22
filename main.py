from model import *
from camera import *

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
from math import *
from PIL import Image
from glm import *
from time import time
from random import random

class test:
    def __init__(self):
        self.i = 0
        pass
 
    def _draw_frame(self):
        self.i += 1
        # self.cam.position.y = sin(self.i/30)
        
        # self.cam.position.y += 0.3
        for i in range(len(self.car_colors)):
            angle = self.i/30 + math.pi*2.0/len(self.car_colors) * i
            self.car.position = vec3(0,0,-5) + vec3(cos(angle),0,sin(angle)) * 3
            self.car.angle = -angle
            self.car.set_color(self.car_colors[i])
            self.cam.render(self.car)
        
        glfw.swap_buffers(self.window)
 
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        
        self.car_colors = []
        for i in range(7):
            self.car_colors.append(random())
        
        self.car = model('models/Chevrolet_Camaro_SS_Low.obj')
        # self.car = model('cube')
        self.car.position = vec3(0,0,-5)
        # self.car.scale = vec3(0.2,0.1,0.4)
        self.car.scale = vec3(0.1)
        
        self.cam = camera()
        self.cam.position = vec3(0,5,0)
        self.cam.target = vec3(0,0,-5)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self._draw_frame()
            glfw.poll_events()

test().main()


