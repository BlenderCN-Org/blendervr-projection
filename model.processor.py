import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Vector, Matrix
    from blendervr.player import device
    from math import radians

    from bge import logic, events

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._all_loaded = False
            self._matrix = Matrix.Identity(4)


        def _checkScenes(self):
            """
            check if all the objects required are in the loaded scenes
            """
            if self._all_loaded:
                return True

            if not self.BlenderVR.isMaster():
                return False

            if not hasattr(logic, 'scenes'):
                return False

            scene_vr = logic.scenes.get('Scene.VR')
            scene_projection = logic.scenes.get('Scene.Projection')

            if not scene_vr or not scene_projection:
                return False

            objects = scene_vr.objects
            self._headtrack_vr_origin = objects.get('HEADTRACK.VR.ORIGIN')
            self._headtrack_vr_head = objects.get('HEADTRACK.VR.HEAD')

            objects = scene_projection.objects
            self._headtrack_projection_origin = objects.get('HEADTRACK.PROJECTION.ORIGIN')
            self._headtrack_projection_head = objects.get('HEADTRACK.PROJECTION.HEAD')

            if \
               self._headtrack_vr_origin and \
               self._headtrack_vr_head and \
               self._headtrack_projection_origin and \
               self._headtrack_projection_head \
               :
                   self._all_loaded = True
                   return True
            else:
                return False

        def run(self):
            """
            run every frame
            """
            if not self._checkScenes():
                return

            self._keyboard()

        def _keyboard(self):
            """handle keyboard events"""

            """
            arrow controls the navigation of the main camera
            (logic.scenes['Scene.VR'].objects['Camera.Parent'])

            but at the moment this is set in the file itself
            the function here is for those without a real head-tracking
            system to try with WASD
            """

            _events = logic.keyboard.events

            x = y = z = 0
            SPEED = 0.005

            if _events[events.WKEY]:
                y -= SPEED

            elif _events[events.SKEY]:
                y += SPEED

            if _events[events.AKEY]:
                x += SPEED

            elif _events[events.DKEY]:
                x -= SPEED

            if _events[events.QKEY]:
                z += SPEED

            elif _events[events.EKEY]:
                z -= SPEED

            if x or y or z:
                try:
                    self._matrix = Matrix.Translation((-x, z, -y)) * self._matrix
                    info = {}
                    info['matrix'] = self._matrix
                    self.user_position(info)

                except Exception as E:
                    self.logger.log_traceback(E)

        def user_position(self, info):
            """
            Callback defined in the XML config file to one of the VRPN Tracker devices
            """
            if not self._checkScenes():
                return

            try:
                #highjack regular head-tracking function
                # do not call: super(Processor, self).user_position(info)

                x, y, z = info['matrix'].translation
                position = Matrix.Translation((z, x, y)).translation

                self._headtrack_vr_head.worldPosition = position + self._headtrack_vr_origin.worldPosition
                self._headtrack_projection_head.worldPosition = position + self._headtrack_projection_origin.worldPosition

            except Exception as E:
                self.logger.log_traceback(E)


elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True

