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
        return lookAt(self.position, self.target, self.up)
    
    def render(self,model):
        model.render(self.view(), self.proj())