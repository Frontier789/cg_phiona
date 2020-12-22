#version 330 core

uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;

in vec3 norm;

out vec4 clr;

void main()
{
    vec3 N = normalize(norm);
    vec3 L = normalize(vec3(1,2,3));
    
    float dp = max(dot(N,L),0.0);
    
    clr = vec4(Ka * 0.05 + dp * Kd, 1);
    
    // clr = vec4(1,1,1,1);
}
