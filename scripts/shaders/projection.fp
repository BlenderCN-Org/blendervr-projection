uniform vec3 head_position;

uniform sampler2D color_NORTH;
uniform sampler2D color_SOUTH;
uniform sampler2D color_EAST;
uniform sampler2D color_WEST;
uniform sampler2D color_ZENITH;
uniform sampler2D color_NADIR;

varying vec4 coord_vec;

/* function from Martinsh Upitis */
vec3 cubeRot(vec3 R)
{
    float x, y, z, texIndex;
    float L = sqrt(2.0) / 2.0;

    // create the normals to check against
    vec3 N1 = vec3(L, L, 0.0);
    vec3 N2 = vec3(-L, L, 0.0);
    vec3 N3 = vec3(0.0, L, L);
    vec3 N4 = vec3(0.0, L, -L);
    vec3 N5 = vec3(L, 0.0, L);
    vec3 N6 = vec3(-L, 0.0, L);

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
        x = -1.0*R.x;
        y = 1.0*R.y;
        z = -1.0*R.z;
        texIndex = 0.0;
    }
    // negative y
    else if (!check1 && !check2 && !check3 && !check4)
    {
        // rotate around x, 180 degrees
        x = 1.0*R.x;
        y = 1.0*R.y;
        z = -1.0*R.z;
        texIndex = 1.0;
    }
    // positive z
    else if (check5 && check6 && check3 && !check4)
    {
        // rotate around x, 90 degrees
        x = -1.0*R.x;
        y = 1.0*R.z;
        z = 1.0*R.y;
        texIndex = 2.0;
    }
    // negative z
    else if (!check5 && !check6 && !check3 && check4)
    {
        // rotate around x, -90 degrees
        x = R.x;
        y = -1.0*R.z;
        z = R.y;
        texIndex = 4.0;
    }
    // negative x
    else if (!check5 && check6 && !check1 && check2)
    {
        // rotate around z, -90 degrees
        x = -1.0*R.z;
        y = -1.0*R.x;
        z = 1.0*R.y;
        texIndex = 3.0;
    }
    // positive x
    else if (check5 && !check6 && check1 && !check2)
    {
        // rotate around z, 90 degrees
        x = 1.0*R.z;
        y = R.x;
        z = 1.0*R.y;
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

    float S1 = atan((x / y),sqrt(3.4));
    float T1 = atan((z / y),sqrt(3.4));
    float S = 0.5 - S1;
    float T = 0.5 - T1;

    return vec3(S, T, texIndex);
}

void main() {
    vec3 world_position = coord_vec.xyz;
    vec3 dir = world_position - head_position;

    dir = normalize(dir);
    vec3 R = cubeRot(dir);

    vec3 col = vec3(0.0);

    if (R.z < 2.0 && R.z > 0.0) {
        col = texture2D(color_EAST,R.xy).rgb;
    }

    else if (R.z < 1.0 ) {
        col = texture2D(color_WEST,R.xy).rgb;
    }

    else if (R.z < 3.0 && R.z > 1.0) {
        col = texture2D(color_ZENITH,R.xy).rgb;
    }

    else if (R.z < 5.0 && R.z > 3.0) {
        col = texture2D(color_NADIR,R.xy).rgb;
    }

    else if (R.z < 4.0 && R.z > 2.0) {
        col = texture2D(color_SOUTH,R.xy).rgb;
    }

    else if (R.z < 6.0 && R.z > 4.0) {
        col = texture2D(color_NORTH,R.xy).rgb;
    }

    gl_FragColor.rgb = col;
    gl_FragColor.a = 1.0;
}
