# BlenderVR Projection

Projection experiments for BlenderVR.
The following is the scene setup required for the scripts to work.

Scene.VR
========

This is the main scene where your VR environment is. We need to add a specific camera rig to the scene in order to the scripts to work.

Logic Bricks
------------

* Always > Python Module Controller (scripts.projection.init)

Objects Hierarchy
-----------------
```
 Camera.Parent
   |
    ---> HEADTRACK.ORIGIN.VR
   |
    ---> Camera.Rig
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
     |
      ---> Camera.NADIR
```

Objects Description
-------------------

* **Camera.Parent** = Empty at 0,0,0

* **HEADTRACK.ORIGIN.VR** = Empty representing the origin of the tracking system in the VR world. Its position is such that when the viewer is standing up, the position info we get should be the same as the Camera.Rig position in relation to the HEADTRACK.ORIGIN.VR

  As an example: if the headtracking system has its origin at the floor, the HEADTRACK.ORIGIN.VR should be at the floor, while the Camera.Rig should be at the same place.
  However if the headtracking system has its origin at a height 0.50, HEADTRACK.ORIGIN.VR should be at 0.50.

* **Camera.Rig** = Empty at the center of the viewer point. Its position will be set dynamically by the headtracking system. Its position is determined by HEADTRACK.ORIGIN.VR position plus the headtracking position.

* **Camera.EAST/WEST/...** = Camera with 90 (degrees, not lens) field of view facing around like a cube map, at the same position as Camera.Rig


Scene.Projection
================

Logic Bricks
------------

* Always > Scene Actuator (Add Background Scene: Scene.VR)
* Always > Python Module Controller (scripts.projection.init)
* Delay (2 tics) > Python Module Controller (scripts.projection.create)
* Always (Pulse True) > Python Module Controller (scripts.projection.loop)

Objects Description
-------------------

* **Camera.Projector** = Active camera, position and parameters matching the projector

* **HEADTRACK.ORIGIN.PROJECTION** = Empty representing the origin of the tracking system in the real world.

  As an example: if the headtracking system has its origin at the floor, the HEADTRACK.ORIGIN.VR should be at the floor.

* **Dummy** = Dummy object with the GLSL material that is always used by the projection planes

* **Dummy.EAST/WEST/...** = Dummy objects with the individual textures we render the Scene.VR cameras to

* **Plane...** = Planes with the GLSL material representing the projection room
