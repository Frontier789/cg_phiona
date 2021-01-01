#version 330 core

layout(location = 0) in vec3 pos;
uniform mat4 view;
uniform mat4 proj;

out vec3 dir;

void main() {
    vec4 vp = proj * view * vec4(pos * 100.0, 0.0);
    vp.z = vp.w;
    
    gl_Position = vp;
    
    dir = pos;
}