import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import shaders
from OpenGL.GL import *
from glm import *

class car:
    def __init__(self):
        poses = cube_positions()
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = vbo.VBO(poses)
        self.__create_shaders()
        self.model_matrix = mat4()
        
    def __create_shaders(self):
        with open("shaders/car.vert",'r') as fv, open("shaders/car.frag",'r') as ff:
            vert = shaders.compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = shaders.compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader = shaders.compileProgram(vert,frag)
            self.loc_MVP = glGetUniformLocation(self.shader, "MVP")
    
    def render(self, view_proj):
        """Render the car."""

        shaders.glUseProgram(self.shader)
        # glUniformMatrix4fv(self.loc_MVP, 1, GL_TRUE, value_ptr(view_proj * self.model_matrix))
        

        self.vbo.bind()
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0)

        glDrawArrays(GL_TRIANGLES, 0, 6)
        
        
def cube_positions():
    # return np.array([-1,-1,-1,-1,-1, 1,-1, 1, 1,1, 1,-1,-1,-1,-1,-1, 1,-1,1,-1, 1,-1,-1,-1,1,-1,-1,1, 1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1,-1, 1,-1,1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1,1,-1, 1,1, 1, 1,1,-1,-1,1, 1,-1,1,-1,-1,1, 1, 1,1,-1, 1,1, 1, 1,1, 1,-1,-1, 1,-1,1, 1, 1,-1, 1,-1,-1, 1, 1,1, 1, 1,-1, 1, 1,1,-1, 1])
    return np.array([-1,-1, -1,1, 1,1,  -1,1, 1,1, 1,-1])

def test():
    c = car()
