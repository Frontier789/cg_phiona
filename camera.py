import math
from glm import *

class camera:
    def __init__(self):
        self.position = vec3()
        self.target   = vec3(0,0,-1)
        self.up       = vec3(0,1,0)
        self.fov      = radians(60.0)
        self.aspect   = 1024 / 768
        self.znear    = 1
        self.zfar     = 100
    
    def proj(self):
        return perspective(self.fov, self.aspect, self.znear, self.zfar)
    
    def view(self):
        v = normalize(self.target - self.position)
        r = normalize(cross(v,self.up))
        u = cross(r,v)
        return inverse(mat4(vec4(r,0),vec4(u,0),vec4(-v,0), vec4(0,0,0,1))) * translate(mat4(), -self.position)