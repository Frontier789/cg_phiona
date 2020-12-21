#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 nrm;
uniform mat4 view;
uniform mat4 model;
uniform mat4 proj;
uniform mat4 norm_mat;

out vec3 norm;

void main() {
    gl_Position = proj * view * model * vec4(pos, 1.0);
    
    norm = vec3(norm_mat * vec4(nrm,0.0));
}