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
