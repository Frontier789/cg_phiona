import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glm import *
from ctypes import c_float, c_uint16, c_void_p, cast, sizeof
from draw import draw
from colorsys import rgb_to_hsv, hsv_to_rgb
from PIL import Image

def gen_vao():
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    return vao

class envbox:
    def __init__(self):
        self.buffers = []
        
        poses = cube_positions()
        
        self.vao = gen_vao()
        self.__make_envbox_vbo(0,poses,3)
        
        self.__create_shaders()
        
        self.cam_pos = vec3()
        
        self.tex = self.__load_tex("models/grass.jpg")
    
    def __make_envbox_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        self.buffers.append(buffer)
    
    def __create_shaders(self):
        with open("shaders/envbox.vert",'r') as fv, open("shaders/envbox.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader = compileProgram(vert,frag)
            self.uview  = glGetUniformLocation(self.shader, "view")
            self.uproj  = glGetUniformLocation(self.shader, "proj")
            self.ucamp  = glGetUniformLocation(self.shader, "cam_pos")
            self.ugrass = glGetUniformLocation(self.shader, "grass")
            
            glUseProgram(self.shader)
            glUniform1i(self.ugrass, 0)
    
    def __load_tex(self,name):
        img = Image.open(name)
        width, height, img_data = img.size[0], img.size[1], img.tobytes("raw", "RGB", 0, -1)

        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        return tex
    
    def set_cam_pos(self,p):
        self.cam_pos = p
    
    def render(self, view, proj):
        """Render the model."""
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.uview, 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
        
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        
        glUniform3f(self.ucamp, self.cam_pos.x,self.cam_pos.y,self.cam_pos.z)
        
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