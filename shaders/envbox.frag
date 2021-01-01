#version 330 core

uniform vec3 cam_pos;
uniform sampler2D grass;

const float exponent = 10.0;
const vec4 ground_color = vec4(vec3(113.0, 108.0, 105.0)/255.0/4.0, 1.0);
const vec4 sky_tint = vec4(vec3(0.1,0.2,0.4)*1.6,1.0);
const vec4 top_tint = vec4(vec3(0.1,0.2,0.4)*0.3,1.0);

in vec3 dir;

void main() {
    vec3 d = normalize(dir);
    
    if (d.y >= 0.0) {
        float p1 = pow(min(1.0, 1.0 - d.y), exponent);
        float p2 = pow(max(0.0, d.y), 2.0);

        gl_FragColor = mix(mix(sky_tint, ground_color, p1), top_tint, p2);
    } else {
        float t = -1.0 *  cam_pos.y / d.y;
        
        vec3 p = cam_pos + d * t;
        
        vec4 c = texture(grass, fract(p.xz/2.0));
        
        vec2 m = sin(p.xz*2.0);
        float w = pow(abs(m.y),0.3) * pow(abs(m.x),0.3) * sign(m.x) * sign(m.y);
        
        c.xyz += vec3(w)*0.06;
        
        gl_FragColor = mix(ground_color,c,exp(-abs(t)/4.0));
    }
}