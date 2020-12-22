#version 330 core

in vec3 norm;

out vec4 clr;

void main()
{
    vec3 N = normalize(norm);
    vec3 L = normalize(vec3(1,2,3));
    
    float dp = dot(N,L);
    
    clr = vec4(vec3(max(dp,0.1)), 1);
    
    // clr = vec4(1,1,1,1);
}
