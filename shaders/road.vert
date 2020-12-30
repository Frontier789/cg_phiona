#version 330 core

layout(location = 0) in vec2 cp;
uniform mat4 view;
uniform mat4 proj;

uniform float t;
uniform float car_speed;
uniform float lanes;
uniform float arc_len;
uniform float ring_radius;
uniform float lane_width;

#define PI 3.14159265358979

out vec2 tpt;

vec3 cp_wp(vec2 p) {
    float angle = PI * 2.0 * (t * car_speed + p.y / (lanes - 1.0) * arc_len);
    return vec3(0.0,-0.04,-5.0) + vec3(cos(angle), 0, sin(angle)) * (ring_radius + p.x * lane_width);
}

void main() {
    vec3 p = cp_wp(cp);
    
    tpt = cp;
    
    gl_Position = proj * view * vec4(p, 1.0);
}