import blendervr

VRPN_DEBUG = True

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
                   self._vrpn_proxy_init()
                   return True
            else:
                return False

        def run(self):
            """
            run every frame
            """

            self._keyboard_vrpn_proxy()

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

        def _vrpn_proxy_init(self):
            """
            initialize fake vrpn inputs based on initial proxy positions
            """
            if not VRPN_DEBUG:
                return

            position = self._headtrack_projection_head.worldPosition - self._headtrack_projection_origin.worldPosition
            x,y,z = position.xyz

            self._matrix = Matrix.Translation((-x, z, -y))
            self._headtrack_vr_head.worldPosition = position + self._headtrack_vr_origin.worldPosition


        def _keyboard_vrpn_proxy(self):

            """
            Keyboard controls the player (hacking VRPN messages)
            with XCV (x,y,z) and Shift+XCV (-x,-y,-z)
            """
            if not VRPN_DEBUG:
                return

            _events = logic.keyboard.events

            x = y = z = 0
            SPEED = 0.01

            if _events[events.XKEY]:
                x += SPEED

            if _events[events.CKEY]:
                y += SPEED

            if _events[events.VKEY]:
                z += SPEED


            if x or y or z:
                try:
                    if _events[events.LEFTSHIFTKEY]: # camera rotation
                        x = -x
                        y = -y
                        z = -z

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

                if abs(x)>=0.01 or abs(y)>=0.01 or abs(z)>=0.01:
                # to remove: mockup as VRPN sever kept sending me (0,0,0) packets in between real (x,y,z) (DPQ)

                    # leaving here for debugging, I need to refresh myself on what is the swizzle needed in BlenderVR
                    #self.logger.info('Raw Data >> x: {0:.2f}, y: {1:.2f}, z: {2:.2f}'.format(x, y, z))

                    position = Matrix.Translation((-z, -x, y)).translation
                    # self.logger.debug(position)
                    self._headtrack_vr_head.worldPosition = position + self._headtrack_vr_origin.worldPosition
                    self.logger.info(self._headtrack_vr_head.worldPosition)
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
