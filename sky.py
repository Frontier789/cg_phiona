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

class sky:
    def __init__(self):
        self.buffers = []
        
        poses = cube_positions()
        
        self.vao = gen_vao()
        self.__make_sky_vbo(0,poses,3)
        
        self.__create_shaders()
    
    def __del__(self):
        glDeleteBuffers(len(self.buffers), self.buffers)
    
    def __make_sky_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        self.buffers.append(buffer)
    
    def __create_shaders(self):
        with open("shaders/sky.vert",'r') as fv, open("shaders/sky.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader  = compileProgram(vert,frag)
            self.uview   = glGetUniformLocation(self.shader, "view")
            self.uproj   = glGetUniformLocation(self.shader, "proj")
            self.usky    = glGetUniformLocation(self.shader, "sky_color")
            self.uground = glGetUniformLocation(self.shader, "ground_color")
    
    def render(self, view, proj):
        """Render the model."""
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.uview, 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
        
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)

def cube_positions():
    return np.array([-1,-1,-1,  -1,-1, 1,  -1, 1, 1, 
                      1, 1,-1,  -1,-1,-1,  -1, 1,-1,
                      1,-1, 1,  -1,-1,-1,   1,-1,-1,
                      1, 1,-1,   1,-1,-1,  -1,-1,-1,
                     -1,-1,-1,  -1, 1, 1,  -1, 1,-1,
                      1,-1, 1,  -1,-1, 1,  -1,-1,-1,
                     -1, 1, 1,  -1,-1, 1,   1,-1, 1,
                      1, 1, 1,   1,-1,-1,   1, 1,-1,
                      1,-1,-1,   1, 1, 1,   1,-1, 1,
                      1, 1, 1,   1, 1,-1,  -1, 1,-1,
                      1, 1, 1,  -1, 1,-1,  -1, 1, 1,
                      1, 1, 1,  -1, 1, 1,   1,-1, 1],np.float32)