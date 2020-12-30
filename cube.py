import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glm import *
from ctypes import c_float, c_uint16, c_void_p, cast, sizeof
from model import model, gen_vao, rotate_clr
from draw import draw

class cube(model):
    def __init__(self):
        super().__init__(("shaders/car.vert","shaders/car.frag"))
        
        poses = cube_positions()
        norms = cube_normals()
        
        vao = gen_vao()
        self.__make_cube_vbo(0,poses,3)
        self.__make_cube_vbo(1,norms,3)
        self.draws.append(draw(vao, 36, vec3(0.06), vec3(0.5), vec3(1)))
        
        self.uKa = glGetUniformLocation(self.shader, "Ka")
        self.uKd = glGetUniformLocation(self.shader, "Kd")
        self.uKs = glGetUniformLocation(self.shader, "Ks")
    
    def set_color(self,color):
        for d in self.draws:
            d.Kd = rotate_clr(d.Kd, color - self.color)
        self.color = color
    
    def __make_cube_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        self.buffers.append(buffer)
    
    def __set_uniforms(self, d):
        glUniform3f(self.uKa, d.Ka.x,d.Ka.y,d.Ka.z)
        glUniform3f(self.uKd, d.Kd.x,d.Kd.y,d.Kd.z)
        glUniform3f(self.uKs, d.Ks.x,d.Ks.y,d.Ks.z)
        
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

def cube_normals():
    p = cube_positions()
    a = []
    for i in range(len(p) // 9):
        A = vec3(p[i*9 + 0],p[i*9 + 1],p[i*9 + 2])
        B = vec3(p[i*9 + 3],p[i*9 + 4],p[i*9 + 5])
        C = vec3(p[i*9 + 6],p[i*9 + 7],p[i*9 + 8])
        n = normalize(cross(A-B,A-C)).to_list()
        a = a + n + n + n
        
    return np.array(a, np.float32)