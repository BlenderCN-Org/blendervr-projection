uniform vec3 head_position;

uniform sampler2D color_NORTH;
uniform sampler2D color_SOUTH;
uniform sampler2D color_EAST;
uniform sampler2D color_WEST;
uniform sampler2D color_ZENITH;
uniform sampler2D color_NADIR;

varying vec4 coord_vec;

/* continous cube mapping by Cindy M. Grimm Bill Niebruegge */

vec3 cubeRot(vec3 R)
{
    float x, y, z, texIndex;
    float L = sqrt(2.0) / 2.0;

    // create the normals to check against
    vec3 N1 = vec3(  L, L,   0.0);
    vec3 N2 = vec3( -L, L,   0.0);
    vec3 N3 = vec3(0.0, L,   L);
    vec3 N4 = vec3(0.0, L,  -L);
    vec3 N5 = vec3(  L, 0.0, L);
    vec3 N6 = vec3( -L, 0.0, L);

    R = normalize(R);

    bool check1 = bool(ceil(dot(N1, R)));
    bool check2 = bool(ceil(dot(N2, R)));
    bool check3 = bool(ceil(dot(N3, R)));
    bool check4 = bool(ceil(dot(N4, R)));
    bool check5 = bool(ceil(dot(N5, R)));
    bool check6 = bool(ceil(dot(N6, R)));

    // positive y
    if (check1 && check2 && check3 && check4)
    {
        // do nothing
        x = R.x;
        y = R.y;
        z = R.z;
        texIndex = 0.0;
    }
    // negative y
    else if (!check1 && !check2 && !check3 && !check4)
    {
        // rotate around x, 180 degrees
        x =  R.x;
        y = -R.y;
        z = -R.z;
        texIndex = 1.0;
    }
    // positive z
    else if (check5 && check6 && check3 && !check4)
    {
        // rotate around x, 90 degrees
        x =  R.x;
        y =  R.z;
        z = -R.y;
        texIndex = 2.0;
    }
    // negative z
    else if (!check5 && !check6 && !check3 && check4)
    {
        // rotate around x, -90 degrees
        x =  R.x;
        y = -R.z;
        z =  R.y;
        texIndex = 3.0;
    }
    // negative x
    else if (!check5 && check6 && !check1 && check2)
    {
        // rotate around z, -90 degrees
        x =  R.y;
        y = -R.x;
        z =  R.z;
        texIndex = 4.0;
    }
    // positive x
    else if (check5 && !check6 && check1 && !check2)
    {
        // rotate around z, 90 degrees
        x = -R.y;
        y =  R.x;
        z =  R.z;
        texIndex = 5.0;
    }
    else
    {
        // do nothing
        x = 0.0;
        y = 0.0;
        z = 0.0;
        texIndex = 6.0;
    }

    float S1 = atan((x/y), sqrt(2.0));
    float S2 = 2.0 * asin(1.0 / sqrt(3.0));
    float S = 0.5 + (S1 / S2);
    float T = ( 1.0 + (asin(z) /
    ( asin(1.0 / (sqrt (2.0 + (x / y)*(x / y) ) ) ) ) ) ) / 2.0;

    return vec3(S, T, texIndex);
}

void main() {
    vec3 world_position = coord_vec.xyz;
    vec3 dir = world_position - head_position;

    dir = normalize(dir);
    vec3 R = cubeRot(dir);

    vec2 uv = R.st;
    float texIndex = R.z;

    vec3 col = vec3(0.0);

    // positive y
    if (texIndex == 0.0) {
        col = texture2D(color_WEST, uv).rgb;
    }

    // negative y
    else if (texIndex == 1.0) {
        col = texture2D(color_EAST, uv).rgb;
    }

    // positive z
    else if (texIndex == 2.0) {
        col = texture2D(color_ZENITH, uv).rgb;
    }

    // negative z
    else if (texIndex == 3.0) {
        col = texture2D(color_NADIR, uv).rgb;
    }

    // negative x
    else if (texIndex == 4.0) {
        col = texture2D(color_SOUTH, uv).rgb;
    }

    // positive x
    else if (texIndex == 5.0) {
        col = texture2D(color_NORTH, uv).rgb;
    }

    gl_FragColor.rgb = col;
    gl_FragColor.a = 1.0;
}
