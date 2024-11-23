#version 330 core //version

in vec3 fragmentColor; // The color of the current coordinate/
in vec2 fragmentTexCoord; // The texture coordinate which we will use in the sampler2D lookup.

out vec4 color; // The color we are outputting.

uniform sampler2D imageTexture; // The texture which the shader is provided.
uniform sampler2D bottom; // The texture which the shader is provided.
uniform sampler2D caustic; // The texture which the shader is provided.
uniform sampler2D noise; // The texture which the shader is provided.
uniform float time;

void main() {

    float noisev = texture( noise, fragmentTexCoord + time * 0.1 ).r;
    float noisev2 = texture( noise, fragmentTexCoord + time * 0.2 ).r;
    vec2 uvnoise = 2.0 * vec2(noisev) - vec2(1.0);

    float edge = pow( texture( caustic, fragmentTexCoord  + uvnoise * 0.05  ).r, 2.0 ) * noisev2 * 0.4;


    color = vec4( 27.0, 188.0, 230.0, 255.0 ) / 255.0 + edge;
    color *= texture(bottom, fragmentTexCoord + uvnoise * 0.05);
    color *= 2.0;
}