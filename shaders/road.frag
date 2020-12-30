#version 330 core

in vec2 tpt;

out vec4 clr;

void main()
{
    float f = fract(tpt.x);
    f = pow(smoothstep(0.0,1.0,1.0 - 2.0 * abs(f - 0.5)),8.0);
    
    clr = vec4(vec3(f),1);
}
