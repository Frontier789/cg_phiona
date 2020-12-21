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
        self.vbo = self.__make_vbo(0,poses,3)
        
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
            self.uproj = glGetUniformLocation(self.shader, 'proj')
            self.umodel_view = glGetUniformLocation(self.shader, "model_view")
    
    def render(self, view, proj):
        """Render the model."""
        
        model = rotate(translate(mat4(), self.position),self.angle,vec3(0,1,0))
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.umodel_view, 1, GL_FALSE, value_ptr(model * view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))

        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        
        
def cube_positions():
    return np.array([-1,-1,-1,-1,-1, 1,-1, 1, 1,1, 1,-1,-1,-1,-1,-1, 1,-1,1,-1, 1,-1,-1,-1,1,-1,-1,1, 1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1,-1, 1,-1,1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1,1,-1, 1,1, 1, 1,1,-1,-1,1, 1,-1,1,-1,-1,1, 1, 1,1,-1, 1,1, 1, 1,1, 1,-1,-1, 1,-1,1, 1, 1,-1, 1,-1,-1, 1, 1,1, 1, 1,-1, 1, 1,1,-1, 1],np.float32)
