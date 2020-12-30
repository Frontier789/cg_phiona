#version 330 core

const float exponent = 10.0;
const vec4 ground_color = vec4(vec3(113.0, 108.0, 105.0)/255.0/4.0, 1.0);
const vec4 sky_tint = vec4(vec3(0.1,0.2,0.4)*1.6,1.0);
const vec4 top_tint = vec4(vec3(0.1,0.2,0.4)*0.3,1.0);

in vec3 dir;

void main() {
    vec3 d = normalize(dir);
    
    float p1 = pow(min(1.0, 1.0 - d.y), exponent);
    float p2 = pow(max(0.0, d.y), 2.0);

    gl_FragColor = mix(mix(sky_tint, ground_color, p1), top_tint, p2);
    
}