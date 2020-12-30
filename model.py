import numpy as np
from OpenGL.arrays import vbo
from OpenGL.GL import *
from OpenGL.GL.shaders import *
from glm import *
from pywavefront import *
from ctypes import c_float, c_uint16, c_void_p, cast, sizeof
import logging
from draw import draw
from colorsys import rgb_to_hsv, hsv_to_rgb

logging.getLogger("pywavefront").setLevel(logging.ERROR)

def gen_vao():
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    return vao

def rotate_clr(clr,r):
    hsv = list(rgb_to_hsv(clr.x,clr.y,clr.z))
    hsv[0] = (hsv[0] + r + 1) % 1.0
    return vec3(hsv_to_rgb(*hsv))

class model:
    def __init__(self, name):
        self.buffers = []
        self.draws   = []
        self.color   = 0.0
        
        if name == 'cube':
            poses = cube_positions()
            norms = cube_normals()
            
            vao = gen_vao()
            self.__make_cube_vbo(0,poses,3)
            self.__make_cube_vbo(1,norms,3)
            self.draws.append(draw(vao, 36, vec3(0.5,0.15,0.1)*5, vec3(0.5,0.15,0.1), vec3(1)))
        else:
            scene = Wavefront(name)
            for mesh in scene.mesh_list:
                for mat in mesh.materials:
                    if mat.vertex_format == 'N3F_V3F':
                        self.__add_drawmat(mat)
                    else:
                        print("unhandled vertex format: ", mat.vertex_format)
        
        self.__create_shaders()
        self.position     = vec3()
        self.angle        = 0.0
        self.scale        = vec3(1)
    
    def set_color(self,color):
        for d in self.draws:
            d.Kd = rotate_clr(d.Kd, color - self.color)
            d.Ka = rotate_clr(d.Ka, color - self.color)
            d.Ks = rotate_clr(d.Ks, color - self.color)
        self.color = color
    
    def __add_drawmat(self,mat):
        vao = gen_vao()
        self.draws.append(draw(vao, len(mat.vertices)//6, vec3(mat.ambient), vec3(mat.diffuse), vec3(mat.specular)))
        data = np.array(mat.vertices, np.float32)
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, cast(3 * 4, c_void_p))
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)
        self.buffers.append(buffer)
    
    def __make_cube_vbo(self,id,data,dim):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(id)
        glVertexAttribPointer(id, dim, GL_FLOAT, GL_FALSE, 0, None)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(data), data, GL_STATIC_DRAW)
        self.buffers.append(buffer)
    
    def __create_shaders(self):
        with open("shaders/car.vert",'r') as fv, open("shaders/car.frag",'r') as ff:
            vert = compileShader(fv.read(), GL_VERTEX_SHADER)
            frag = compileShader(ff.read(), GL_FRAGMENT_SHADER)
            
            self.shader = compileProgram(vert,frag)
            self.uproj = glGetUniformLocation(self.shader, "proj")
            self.umodel = glGetUniformLocation(self.shader, "model")
            self.uview = glGetUniformLocation(self.shader, "view")
            self.unorm = glGetUniformLocation(self.shader, "norm_mat")
            self.uKa = glGetUniformLocation(self.shader, "Ka")
            self.uKd = glGetUniformLocation(self.shader, "Kd")
            self.uKs = glGetUniformLocation(self.shader, "Ks")
    
    def model_matrix(self):
        return scale(rotate(translate(mat4(), self.position),self.angle,vec3(0,1,0)),self.scale)
    
    def render(self, view, proj):
        """Render the model."""
        
        model = self.model_matrix()
        normm = inverse(transpose(model))
        
        glUseProgram(self.shader)
        glUniformMatrix4fv(self.umodel, 1, GL_FALSE, value_ptr(model))
        glUniformMatrix4fv(self.uview, 1, GL_FALSE, value_ptr(view))
        glUniformMatrix4fv(self.uproj, 1, GL_FALSE, value_ptr(proj))
        glUniformMatrix4fv(self.unorm, 1, GL_FALSE, value_ptr(normm))
        
        for d in self.draws:
            glBindVertexArray(d.vao)
            glUniform3f(self.uKa, d.Ka.x,d.Ka.y,d.Ka.z)
            glUniform3f(self.uKd, d.Kd.x,d.Kd.y,d.Kd.z)
            glUniform3f(self.uKs, d.Ks.x,d.Ks.y,d.Ks.z)
            glDrawArrays(GL_TRIANGLES, 0, d.vert_count)
        
        
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