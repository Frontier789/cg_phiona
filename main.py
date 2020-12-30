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
from road import road

class View:
    GLOBAL = 0
    FOLLOW_CAR = 1
    NUM_VIEWS = 2
    def next_view(self):
        return (self + 1) % View.NUM_VIEWS

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
arc_len  = 0.15
car_size = 0.03
car_speed   = 0.2
lane_width  = 0.15
ring_radius = 2.0
def cp_wp(p,t):
    angle = math.pi * 2.0 * (t *car_speed + p.y / (lanes - 1) * arc_len)
    # return vec3(0,0,-5) + vec3(cos(angle), 0, sin(angle)) * (ring_radius + p.x * lane_width)
    # return vec3(0,0,-5) + vec3(cos(angle), 0, angle) * (ring_radius + p.x * lane_width + sin(angle * 10.0)*0.2)
    return vec3(p.x * lane_width + sin(angle / 5.0) * 2.0,-0.04,angle)

def cp_wp_a(p,t):
    p1 = cp_wp(p,t)
    p2 = cp_wp(p,t+0.01)
    v = normalize(p2 - p1)
    return p1, atan2(-v.z,v.x) + math.pi/2

def in_bounds(p):
    return p.x >= 0 and p.x < lanes and p.y >= 0 and p.y < max_y

class test:
    def __init__(self):
        self.i = 0
        self.clock = time()
        self.start_time = time()
        self.view = View.FOLLOW_CAR
        self.done = False
        pass
 
    def __draw_frame(self):
        self.i += 1
        
        t = time()
        
        self.__update_cam(t)
        self.__update_cars(t)
        self.road.set_time(t - self.start_time)
        
        self.__render_cars(t)
        self.cam.render(self.sky)
        self.cam.render(self.road)
        
        glfw.swap_buffers(self.window)
    
    def __update_cam(self,t):
        if self.view == View.FOLLOW_CAR:
            car = self.car_states[0]
            p,a = cp_wp_a(car.curpos(t), t - self.start_time)
            self.car.position = p
            self.car.angle = a
            d = normalize(vec3(self.car.model_matrix() * vec4(0,0,-1,0)))
            u = vec3(0,1,0)
            self.cam.position = p + d + u / 3 * (1 + 0.1 * sin(self.i / 30) * (1 + sin(self.i / 100)) )
            self.cam.target = p
        if self.view == View.GLOBAL:
            p,a = cp_wp_a(vec2(lanes/2, max_y/2), t - self.start_time)
            self.car.position = p
            self.car.angle = a
            d = normalize(vec3(self.car.model_matrix() * vec4(0,0,-1,0)))
            u = vec3(0,1,0)
            self.cam.position = p + d * 3 + u
            self.cam.target = p
    
    def __render_cars(self,t):
        for s in self.car_states:
            p,a = cp_wp_a(s.curpos(t), t - self.start_time)
            self.car.position = p
            self.car.angle = a
            self.car.set_color(s.color)
            self.cam.render(self.car)
    
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
    
    def onkey(self, win, key, scancode, action, mod):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE: 
                self.done = True
            elif key == glfw.KEY_C:
                self.view = View.next_view(self.view)
    
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        glfw.set_key_callback(self.window, self.onkey)
        
        self.car = model('models/Chevrolet_Camaro_SS_Low.obj')
        self.car.scale = vec3(car_size)
        
        # self.car = model('cube')
        # self.car.scale = vec3(0.08,0.01,0.18)
        
        self.sky = sky()
        self.road = road(car_speed,lanes,arc_len,ring_radius,lane_width,max_y)
        
        self.gen_car_states()
        
        self.cam = camera()
        self.cam.position = vec3(0,3,0)
        self.cam.target = vec3(0,0,-5)
        
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        
        while not glfw.window_should_close(self.window) and not self.done:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.__draw_frame()
            glfw.poll_events()
        

test().main()


