#version 330 core

uniform vec3 Ka;
uniform vec3 Kd;
uniform vec3 Ks;
uniform vec3 cam_pos;
uniform float Ns = 9.0;

in vec3 norm;
in vec3 wp;

out vec4 clr;

void main()
{
    vec3 L = normalize(vec3(0,3,-1));
    vec3 n = normalize(norm);

    vec3 V = normalize(cam_pos - wp);
    vec3 R = reflect(-L, n);
    vec3 specular = pow(max(dot(V, R), 0.0), Ns) * Ks;

    vec3 diffuse = max(dot(n,L),0) * Kd;

    clr = vec4(Ka * 0.05 + diffuse + specular,1);
}
