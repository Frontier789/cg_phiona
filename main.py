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
from random import random, randint, choice
from sky import sky

class View:
    GLOBAL = 1
    FOLLOW_CAR = 2

class car_state:
    def __init__(self, pos, t=1.0, color = None):
        self.pos = pos
        self.color = random() if color is None else color
        self.target = pos
        self.tt = t
        self.clock = time()
    
    def move_delta(self, delta):
        self.move(self.target + delta)
    
    def move(self, pos):
        self.pos    = self.curpos(time())
        self.target = pos
        self.clock  = time()
    
    def curpos(self,t):
        r = (t - self.clock) / self.tt
        if r > 1.0:
            return self.target
        return self.target * r + self.pos * (1.0 - r)

num_cars = 13
max_y    = 14
lanes    = 4
arc_len  = 0.1
car_size = 0.03
car_speed   = 0.2
lane_width  = 0.1
ring_radius = 2.0
def cp_wp(p,t):
    angle = math.pi * 2.0 * (t *car_speed + p.y / (lanes - 1) * arc_len)
    return vec3(0,0,-5) + vec3(cos(angle), 0, sin(angle)) * (ring_radius + p.x * lane_width), -angle

def in_bounds(p):
    return p.x >= 0 and p.x < lanes and p.y >= 0 and p.y < max_y

class test:
    def __init__(self):
        self.i = 0
        self.clock = time()
        self.start_time = time()
        self.view = View.GLOBAL
        pass
 
    def __draw_frame(self):
        self.i += 1
        
        t = time()
        
        self.__update_cam(t)
        self.__update_cars(t)
        self.__render_cars(t)
        self.__render_sky()
        
        glfw.swap_buffers(self.window)
    
    def __update_cam(self,t):
        if self.view == View.FOLLOW_CAR:
            car = self.car_states[0]
            p,a = cp_wp(car.curpos(t), t - self.start_time)
            self.car.position = p
            self.car.angle = a
            d = normalize(vec3(self.car.model_matrix() * vec4(0,0,-1,0)))
            u = vec3(0,1,0)
            self.cam.position = p + d + u / 3 * sin(self.i / 30)
            self.cam.target = p
        if self.view == View.GLOBAL:
            self.cam.position = vec3(0,3,0)
            self.cam.target = vec3(0,0,-5)
    
    def __render_cars(self,t):
        for s in self.car_states:
            p,a = cp_wp(s.curpos(t), t - self.start_time)
            self.car.position = p
            self.car.angle = a
            self.car.set_color(s.color)
            self.cam.render(self.car)
    
    def __render_sky(self):
        self.cam.render(self.sky)
    
    def __update_cars(self,t):
        if t - self.clock > 0.1:
            if random() < 0.9:
                i = randint(0, num_cars-1)
                d = [vec2(1,0),vec2(-1,0),vec2(0,1),vec2(0,-1)]
                d = choice(d)
                if in_bounds(d + self.car_states[i].target):
                    ok = True
                    for j in range(num_cars):
                        ok = ok and not self.cars_close(i,j,d)
                    if ok:
                        self.car_states[i].move_delta(d)
            self.clock = t
    
    def cars_close(self,i,j,d):
        if i == j:
            return False
        p = self.car_states[i].target + d
        q = self.car_states[j].target
        return length(p-q) < (lane_width + arc_len / max_y) / 4.0
    
    def gen_car_states(self):
        self.car_states = []
        for i in range(num_cars):
            p = vec2(randint(0,lanes-1), randint(0, max_y-1))
            self.car_states.append(car_state(p))
    
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        
        self.car = model('models/Chevrolet_Camaro_SS_Low.obj')
        self.car.scale = vec3(car_size)
        
        self.sky = sky()
        
        self.gen_car_states()
        
        self.cam = camera()
        self.cam.position = vec3(0,3,0)
        self.cam.target = vec3(0,0,-5)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.__draw_frame()
            glfw.poll_events()

test().main()


