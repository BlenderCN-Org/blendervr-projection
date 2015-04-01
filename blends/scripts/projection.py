
from bge import logic
from bge import texture as VT 

def init_scene():
    if not hasattr(logic, "scenes"):
        logic.scenes = {}

    scene = logic.getCurrentScene()
    logic.scenes[scene.name] = scene


class Wall:
    def __init__(self, scene_main, scene_projection, name):
        obj = scene_projection.objects.get('Plane.{0}'.format(name))

        # get the reference pointer (ID) of the texture
        mat_id = VT.materialID(obj, 'IM{0}'.format(name))

        # create a texture object
        self._texture = VT.Texture(obj, mat_id)

        # create a new source
        camera = scene_main.objects.get('Camera.{0}'.format(name))
        source = VT.ImageRender(scene_main, camera)
        #source.background = (180, 90, 144, 10)

        # update/replace the texture
        self._texture.source = source
        self._texture.refresh(False)

    def refresh(self):
        self._texture.refresh(False)


class ProjectionVR():
    def __init__(self, scene, objects, name):
        obj = objects.get('Dummy.{0}'.format(name))

        # get the reference pointer (ID) of the texture
        mat_id = VT.materialID(obj, 'MAVR.{0}'.format(name))

        # create a texture object
        self._texture = VT.Texture(obj, mat_id)

        # create a new source
        camera = scene.objects.get('Camera.{0}'.format(name))
        source = VT.ImageRender(scene, camera)

        # update/replace the texture
        self._texture.source = source
        self._texture.refresh(False)


    def refresh(self):
        self._texture.refresh(False)


class ProjectionsVR():
    def __init__(self, scene, objects):
        self._views = []

        for view in {'NORTH', 'SOUTH', 'EAST', 'WEST', 'ZENITH', 'NADIR'}:
            self._views.append(ProjectionVR(scene, objects, view))

    def update(self):
        for view in self._views:
            view.refresh()


class ShaderObject():
    _VertexShader = """
varying vec4 coord_vec;

void main() {
    coord_vec = gl_Vertex;
    gl_Position = gl_ModelViewProjectionMatrix * coord_vec;
}
"""

    _FragmentShader = """
uniform vec3 camera_position;

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
    vec3 dir = world_position - camera_position;

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
"""
    def __init__(self, reference, shader_object):
        self._reference = reference
        self._reference_position = reference.worldPosition
        self._shader_object = shader_object

        self.update()


    def _shader(self):
        for mesh in self._shader_object.meshes:
            for material in mesh.materials:
                shader = material.getShader()

            if shader != None:
                if not shader.isValid():
                    shader.setSource(self._VertexShader, self._FragmentShader, True)

                shader.setUniformfv('camera_position', self._reference_position)

                shader.setSampler('color_NORTH', 0)
                shader.setSampler('color_SOUTH', 1)
                shader.setSampler('color_EAST', 2)
                shader.setSampler('color_WEST', 3)
                shader.setSampler('color_ZENITH', 4)
                shader.setSampler('color_NADIR', 5)


    def update(self):
        self._reference_position = self._reference.worldPosition
        self._shader()


def create():
    """
    Create dynamic textures
    """

    if hasattr(logic, "walls"):
        remove()

    scenes = logic.scenes

    scene_main = scenes['Scene']
    scene_projection = scenes['Scene.projection']

    dummy_objects = {obj.name : obj for obj in scene_projection.objects if obj.name.startswith("Dummy.") }
    logic.projection = ProjectionsVR(scene_main, dummy_objects)

    logic.shader_object = ShaderObject(
            scene_projection.objects.get('CAMERA_REFERENCE'),
            scene_projection.objects.get('Dummy'),
            )


def loop():
    """
    render to texture
    from each of the cameras, to each of their corresponding textures
    """
    if hasattr(logic, "projection"):
        logic.projection.update()


    if hasattr(logic, "shader_object"):
        logic.shader_object.update()


def remove():
    """
    reset the planes to their original textures
    """
    if hasattr(logic, "projection"):
        del logic.projection
