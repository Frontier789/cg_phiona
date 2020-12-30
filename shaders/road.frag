#version 330 core

uniform float t;
uniform float lanes;
uniform float car_speed;
uniform float ring_radius;

in vec2 tpt;

out vec4 clr;

#define LANE_WIDTH 0.1
#define LANE_AA 0.02

#define STRIP_LENGTH 0.3
#define STRIP_AA 0.02

#define PI 3.14159265358979

void main()
{
    float f = fract(tpt.x);
    f = 1.0 - 2.0 * abs(f - 0.5);
    if (f > 1.0 - LANE_WIDTH) {
        f = 1.0;
    } else if (f > 1.0 - LANE_WIDTH - LANE_AA) {
        f = (f - (1.0 - LANE_WIDTH - LANE_AA)) / ((1.0 - LANE_WIDTH) - (1.0 - LANE_WIDTH - LANE_AA));
    } else {
        f = 0.0;
    }
    
    float g = fract(tpt.y + PI * 2.0 * t * car_speed * 4.8);
    g = 1.0 - 2.0 * abs(g - 0.5);
    if (g > 1.0 - STRIP_LENGTH) {
        g = 1.0;
    } else if (g > 1.0 - STRIP_LENGTH - STRIP_AA) {
        g = (g - (1.0 - STRIP_LENGTH - STRIP_AA)) / ((1.0 - STRIP_LENGTH) - (1.0 - STRIP_LENGTH - STRIP_AA));
    } else {
        g = 0.0;
    }
    
    if (tpt.x < -0.2 || tpt.x > lanes - 0.8) {
        g = 1.0;
    }
    
    clr = vec4(vec3(f * g),1);
}
