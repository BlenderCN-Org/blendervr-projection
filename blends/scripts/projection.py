
from bge import logic
from bge import texture as VT


# ############################################################
# Video Texture
# ############################################################

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


# ############################################################
# GLSL
# ############################################################

class ShaderObject():
    def __init__(self, reference, shader_object):
        self._reference = reference
        self._reference_position = reference.worldPosition
        self._shader_object = shader_object

        self._vertex_shader = self._openText('shaders/projection.vp')
        self._fragment_shader = self._openText('shaders/projection.fp')

        self.update()

    def _openText(self, path):
        """"""
        import os

        folderpath = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folderpath, path)
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        return data

    def _shader(self):
        for mesh in self._shader_object.meshes:
            for material in mesh.materials:
                shader = material.getShader()

            if shader != None:
                if not shader.isValid():
                    shader.setSource(self._vertex_shader, self._fragment_shader, True)

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


# ############################################################
# Check-Ups
# ############################################################

def check_objects(scenes):
    """
    check if we have all the scenes and all the objects properly created
    """
    scene_vr = scenes.get('Scene.VR')
    scene_projection = scenes.get('Scene.Projection')

    if not scene_vr:
        print("Scene 'Scene.VR' not found. Make sure the scene is calling this init() function")
        return False

    if not scene_projection:
        print("Scene 'Scene.Projection' not found. Make sure the scene is calling this init() function")
        return False

    objects = scene_vr.objects
    for ob in {
        'Camera.Parent',
        'HEADTRACK.VR.ORIGIN',
        'HEADTRACK.VR.HEAD',
        'Camera.EAST',
        'Camera.WEST',
        'Camera.NORTH',
        'Camera.SOUTH',
        'Camera.ZENITH',
        'Camera.NADIR',
      }:
        if not objects.get(ob):
            print("Scene 'Scene.VR' doesn't have object '{0}'".format(ob))
            return False

    objects = scene_projection.objects
    for ob in {
        'HEADTRACK.PROJECTION.ORIGIN',
        'HEADTRACK.PROJECTION.HEAD',
        'Dummy',
        'Dummy.EAST',
        'Dummy.WEST',
        'Dummy.NORTH',
        'Dummy.SOUTH',
        'Dummy.ZENITH',
        'Dummy.NADIR',
      }:
        if not objects.get(ob):
            print("Scene 'Scene.Projection' doesn't have object '{0}'".format(ob))
            return False

    return True


# ############################################################
# Main
# ############################################################

def main():
    """
    Create dynamic textures
    """
    scenes = logic.scenes if hasattr(logic, 'scenes') else {}

    if not check_objects(scenes):
        logic.endGame()
        return

    scene_vr = scenes.get('Scene.VR')
    scene_projection = scenes.get('Scene.Projection')

    dummy_objects = {ob.name : ob for ob in scene_projection.objects if ob.name.startswith("Dummy.") }
    logic.projection = ProjectionsVR(scene_vr, dummy_objects)

    objects = scene_projection.objects
    logic.shader_object = ShaderObject(
            objects.get('HEADTRACK.PROJECTION.HEAD'),
            objects.get('Dummy'),
            )


def init_scene():
    """
    called by each individual scene
    """
    if not hasattr(logic, "scenes"):
        logic.scenes = {}

    scene = logic.getCurrentScene()
    logic.scenes[scene.name] = scene


def loop():
    """
    render to texture
    from each of the cameras, to each of their corresponding textures
    """
    if hasattr(logic, "projection"):
        logic.projection.update()


    if hasattr(logic, "shader_object"):
        logic.shader_object.update()
