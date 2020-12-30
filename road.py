import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glm import *
from ctypes import c_float, c_uint16, c_void_p, cast, sizeof
from draw import draw
from colorsys import rgb_to_hsv, hsv_to_rgb

def gen_vao():
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    return vao

class road:
    def __init__(self,car_speed,lanes,arc_len,ring_radius,lane_width,max_y):
        self.buffers = []
        
        poses = []
        mul = 10
        extx = 0.2
        exty = 20
        
        for j in range(max_y * mul + exty * 2 * mul):
            poses.append(0 - 0.5 - extx)
            poses.append(j / mul - exty)
            poses.append(lanes - 0.5 + extx)
            poses.append(j / mul - exty)
        
        self.verts = len(poses)//2
        
        self.vao = gen_vao()
        self.__make_road_vbo(0,np.array(poses,np.float32),2)
        
        self.__create_shaders(car_speed,lanes,arc_len,ring_radius,lane_width,max_y)
    
    def __make_road_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        self.buffers.append(buffer)
    
    def __create_shaders(self,car_speed,lanes,arc_len,ring_radius,lane_width,max_y):
        with open("shaders/road.vert",'r') as fv, open("shaders/road.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader  = compileProgram(vert,frag)
            self.uview   = glGetUniformLocation(self.shader, "view")
            self.uproj   = glGetUniformLocation(self.shader, "proj")
            
            set_u = lambda var,name: glUniform1f(glGetUniformLocation(self.shader, name), var)
            
            glUseProgram(self.shader)
            set_u(car_speed,"car_speed")
            set_u(lanes,"lanes")
            set_u(arc_len,"arc_len")
            set_u(ring_radius,"ring_radius")
            set_u(lane_width,"lane_width")
            set_u(max_y,"max_y")
            
            self.ut = glGetUniformLocation(self.shader, "t")
    
    def set_time(self,t):
        glUniform1f(self.ut,t)
    
    def render(self, view, proj):
        """Render the model."""
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.uview, 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.verts)
