#version 330 core

layout(location = 0) in vec3 vert;
uniform mat4 model_view;
uniform mat4 proj;

void main() {
    gl_Position = proj * model_view * vec4(vert, 1.0);
}