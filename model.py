import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glm import *

class model:
    def __init__(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        poses = cube_positions()
        norms = cube_normals()
        
        self.poses = self.__make_vbo(0,poses,3)
        self.norms = self.__make_vbo(1,norms,3)
        
        self.__create_shaders()
        self.model_matrix = mat4()
        self.position     = vec3()
        self.angle        = 0.0
    
    def __make_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
    
    def __create_shaders(self):
        with open("shaders/car.vert",'r') as fv, open("shaders/car.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader = compileProgram(vert,frag)
            self.uproj = glGetUniformLocation(self.shader, "proj")
            self.umodel = glGetUniformLocation(self.shader, "model")
            self.uview = glGetUniformLocation(self.shader, "view")
            self.unorm = glGetUniformLocation(self.shader, "norm_mat")
    
    def render(self, view, proj):
        """Render the model."""
        
        model = rotate(translate(mat4(), self.position),self.angle,vec3(0,1,0))
        normm = inverse(transpose(model))
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.umodel, 1, GL_FALSE, value_ptr(model))
        glUniformMatrix4fv(self.uview, 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
        glUniformMatrix4fv(self.unorm, 1, GL_FALSE, value_ptr(normm))

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