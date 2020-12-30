#version 330 core

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 nrm;
uniform mat4 view;
uniform mat4 model;
uniform mat4 proj;
uniform mat4 norm_mat;

out vec3 norm;
out vec3 wp;

void main() {
    vec4 world = model * vec4(pos, 1.0);
    gl_Position = proj * view * world;
    
    wp = vec3(world);
    norm = vec3(norm_mat * vec4(nrm,0.0));
}