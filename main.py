# import glfw
# from OpenGL.GL import *
# from math import *
# from glm import *
# from OpenGL.arrays import vbo
# from OpenGL.GL import shaders
# from car import car

# if not glfw.init():
#     print("Initializing GLFW has failed")
#     exit(1)

# window = glfw.create_window(1024, 768, "Car racer", None, None)
# if not window:
#     print("Creating a window failed")
#     glfw.terminate()
#     exit(1)

# glfw.make_context_current(window)

# persp = perspective(radians(60), 1024/768, 0.1, 10)
# view  = mat4()

# c = car()

# i = 0

# while not glfw.window_should_close(window):
    
#     glClearColor(sin(i/300.0)*0.5+0.5,0,0,1)
#     glClear(GL_COLOR_BUFFER_BIT)
    
#     c.render(mat4())
    
#     glfw.swap_buffers(window)
#     glfw.poll_events()
#     i = i+1

# glfw.terminate()

import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import math
from PIL import Image
from glm import *
from time import time

class car:
    def __create_shaders(self):
        with open("shaders/car.vert",'r') as fv, open("shaders/car.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader = compileProgram(vert,frag)
            self.uproj = glGetUniformLocation(self.shader, 'proj')
            self.umodel_view = glGetUniformLocation(self.shader, "model_view")
            self.uBackgroundTexture = glGetUniformLocation(self.shader, "backgroundTexture")
 
    # initialise opengl
    def _init_opengl(self):
  
        self.__create_shaders()

        # create and bind VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
 
        # generate vertex buffer
        vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer)
 
        # enable vertex attribute array
        glEnableVertexAttribArray(0)
 
        # vertex attribute pointer
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
 
        # buffer vertex data
        vertexData = cube_positions()
        glBufferData(GL_ARRAY_BUFFER, 4 * len(vertexData), vertexData, GL_STATIC_DRAW)
 
        # generate UV buffer
        uvBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, uvBuffer)
 
        # enable UV attribute array
        # glEnableVertexAttribArray(aUV)
 
        # UV attribute pointer
        # glVertexAttribPointer(aUV, 2, GL_FLOAT, GL_FALSE, 0, None)
 
        # buffer UV data
        # uvData = np.array(backgroundUV, np.float32)
        # glBufferData(GL_ARRAY_BUFFER, 4 * len(uvData), uvData, GL_STATIC_DRAW)
 
        # unbind and disable
        glBindVertexArray(0)
        glDisableVertexAttribArray(0)
        # glDisableVertexAttribArray(aUV)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
 
        # # set background texture
        # backgroundImage = Image.open(self.BACKGROUND_IMAGE)
        # backgroundImageData = np.array(list(backgroundImage.getdata()), np.uint8)
          
        # self.backgroundTexture = glGenTextures(1)
        # glBindTexture(GL_TEXTURE_2D, self.backgroundTexture)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        # glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, backgroundImage.size[0], backgroundImage.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, backgroundImageData)
        # glBindTexture(GL_TEXTURE_2D, 0)
        
        glfw.swap_interval(1)
        
        self.i = 0
 
    # draw frame
    def _draw_frame(self):
        self.i += 1
        
        # create modelview matrix
        model_view = translate(mat4(), vec3(0,0,-5)) * rotate(mat4(), self.i/30.0, vec3(0,1,0))
 
        # create projection matrix
        proj = perspective(radians(60.0), 1024 / 768, 1, 100)
 
        # use shader program
        glUseProgram(self.shader)
  
        # set uniforms
        glUniformMatrix4fv(self.umodel_view, 1, GL_FALSE, value_ptr(model_view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
   
        # bind VAO
        glBindVertexArray(self.vao)
 
        # draw
        glDrawArrays(GL_TRIANGLES, 0, 36)
 
        # unbind
        glBindVertexArray(0)
        glUseProgram(0)
 
        # swap buffers
        glfw.swap_buffers(self.window)
 
    # setup and run OpenGL
    def main(self):
        glfw.init()
        self.window = glfw.create_window(1024, 768, "Car racer", None, None)
        glfw.make_context_current(self.window)
        self._init_opengl()
        
        while not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT)
            self._draw_frame()
            glfw.poll_events()
        

def cube_positions():
    return np.array([-1,-1,-1,-1,-1, 1,-1, 1, 1,1, 1,-1,-1,-1,-1,-1, 1,-1,1,-1, 1,-1,-1,-1,1,-1,-1,1, 1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1, 1,-1, 1,-1,1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1, 1,-1,-1, 1,1,-1, 1,1, 1, 1,1,-1,-1,1, 1,-1,1,-1,-1,1, 1, 1,1,-1, 1,1, 1, 1,1, 1,-1,-1, 1,-1,1, 1, 1,-1, 1,-1,-1, 1, 1,1, 1, 1,-1, 1, 1,1,-1, 1],np.float32)

# run an instance of car
car().main()


