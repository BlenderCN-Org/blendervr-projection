
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
        #self._texture.refresh(False)
        self._texture.refresh(True)


def create():
    """
    Create dynamic textures
    """

    if hasattr(logic, "walls"):
        remove()

    logic.walls = []
    scenes = logic.scenes

    scene_main = scenes['Scene']
    scene_projection = scenes['Scene.projection']
    
    views = ['left', 'front', 'floor', 'ceiling', 'right']

    for view in views:
        wall = Wall(scene_main, scene_projection, view)
        logic.walls.append(wall)


def loop():
    """
    render to texture
    from each of the cameras, to each of their corresponding textures
    """
    if hasattr(logic, "walls"):
        for wall in logic.walls:
             wall.refresh()


def remove():
    """
    reset the planes to their original textures
    """
    if hasattr(logic, "walls"):
        del logic.walls


"""
1. look to an example of video texture
2. look to an example of render to texture
3. try the techniques with this example
4. do that with the theatre

"""