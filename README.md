# BlenderVR Projection

Projection experiments for BlenderVR.
The following is the scene setup required for the scripts to work.

Scene.VR
========

This is the main scene where your VR environment is. We need to add a specific camera rig to the scene in order to the scripts to work.
This scene width and height parameters need to be square (ideally a power of 2 like 1024x1024) so that the cubemap capturing is correct.

Logic Bricks
------------

* Always > Python Module Controller (scripts.projection.init_scene)

Objects Hierarchy
-----------------
```
 Camera.Parent
   |
    ---> HEADTRACK.VR.ORIGIN
   |
    ---> HEADTRACK.VR.HEAD
     |
      ---> Camera.EAST
     |
      ---> Camera.WEST
     |
      ---> Camera.NORTH
     |
      ---> Camera.SOUTH
     |
      ---> Camera.ZENITH
     |
      ---> Camera.NADIR
```

Objects Description
-------------------

* **Camera.Parent** = Empty at 0,0,0

* **HEADTRACK.VR.ORIGIN** = Empty representing the origin of the tracking system in the VR world. Its position is such that when the viewer is standing up, the position info we get should be the same as the Camera.Rig position in relation to the HEADTRACK.VR.ORIGIN

  As an example: if the headtracking system has its origin at the floor, the HEADTRACK.VR.ORIGIN should be at the floor, while the HEADTRACK.VR.HEAD should be at the same place.
  However if the headtracking system has its origin at a height 0.50, HEADTRACK.VR.ORIGIN should be at 0.50.

* **HEADTRACK.VR.HEAD** = Empty at the center of the viewer point. Its position will be set dynamically by the headtracking system. Its position is determined by HEADTRACK.VR.ORIGIN position plus the headtracking position.

* **Camera.EAST/WEST/...** = Camera with 90 (degrees, not lens) field of view facing around like a cube map, at the same position as Camera.Rig


Scene.Projection
================

Logic Bricks
------------

* Always > Scene Actuator (Add Background Scene: Scene.VR)
* Always > Python Module Controller (scripts.projection.init_scene)
* Delay (2 tics) > Python Module Controller (scripts.projection.main)
* Always (Pulse True) > Python Module Controller (scripts.projection.loop)

Objects Description
-------------------

* **Camera.Projector** = Active camera, position and parameters matching the projector

* **HEADTRACK.PROJECTION.ORIGIN** = Empty representing the origin of the tracking system in the real world.

  As an example: if the headtracking system has its origin at the floor, the HEADTRACK.VR.ORIGIN should be at the floor.

* **HEADTRACK.PROJECTION.HEAD** = Empty representing the head of the tracking system in the real world. Its position is dynamically set by the headtracking system. Its position is determined by HEADTRACK.PROJECTION.ORIGIN position plus the headtracking position.

* **Dummy** = Dummy object with the GLSL material that is always used by the projection planes

* **Dummy.EAST/WEST/...** = Dummy objects with the individual textures we render the Scene.VR cameras to

* **Plane...** = Planes with the GLSL material representing the projection room

Movements
=========

Navigate the VR Scene
---------------------

1. Scene.VR
  * Move **Camera.Parent**.

Head-Tracking movement
----------------------

1. Scene.VR:
  * Move **HEADTRACK.VR.HEAD**
  * (position = headtracking.position + HEADTRACK.VR.ORIGIN)

2. Scene.Projection:
  * Move **HEADTRACK.PROJECTION.HEAD**
  * (position = headtracking.position + HEADTRACK.PROJECTION.ORIGIN)

Setup Projector
===============

1. If projector has a non null shift (see 'projector shift' in google), blendervr-projection requires
a Blender version that takes into acount Camera shift in BGE. Take the Blender version in BlenderVR trunk for now
(not yet integrated in Blender2.75a, should be integrated in next Blender release).

2. Open model-calibration.blend

3. (modify the representation of the VR architecture to match yours)

4. Go to the screen layout called 'Calibration' (full screen of Projection scene, camera viewpoint,
the .blend should open itself on that very layout)

5. With the projector connected to your computer (duplicate screen, projector resolution),
change camera extrinsic and intrinsic parameters to match projector's. You can also do it in real time (BGE), see next step.
Parameters are:

* Intrinsic: Camera Shift, Zoom

* Extrinsic: Camera Position / Orientation (eventually use your tracking system to know the exact pos/rot of the projector compared to the real screens)

5bis. BGE controls (no need for BlenderVR here, controls defined in .blend file)

* LeftCtrl + [Left,Right,Up,Down] (arrow keys) rotate Camera (in Projection Scene)

* LeftCtrl + [WSADQE] translate Camera (in Projection Scene)

6. Once Real and Virtual match achieved, save the .blend file and open BlenderVR

7. Select a 'bufferless' screen configuration (i.e. one with a buffer set to "none": <graphic_buffer user='user A' buffer="none" eye="middle"/>)

8. Launch BlenderVR, controls are:

* [W,S,A,D,Q,E]: translate BlenderVR user (bypass user_position method, for those without user VRPN tracking enabled)

* [Left,Right] (arrow keys) rotate Camera (in VR Scene)

* [Up,Down] (arrow keys) translate Camera (in VR Scene)

9. Reproduce / append architecture geometry and camera setup in your own scene (e.g. model.blend)
