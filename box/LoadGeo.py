# [Fabian 23Oct15]
# adjust DA_Turntable from /da/proj/paulBourke for loading general geometry

from omega import getDefaultCamera, Color, setEventFunction, setUpdateFunction
from GeometryFile import GeometryFile
from DAEventHandler import DAEventHandler

#fileToLoad = "/da/mannequinShoot/exports/Mook/Mook_mix1_initial.fbx"
#fileToLoad = "/home/fabian/Code/paulBourke/weld/take1.obj"
fileToLoad = "/home/fabian/Code/examples/box/box.obj"
#fileToLoad = "/home/fabian/Code/examples/box/box_translate.obj"

cam = getDefaultCamera()
cam.setControllerEnabled(False)
cam.setPosition(Vector3(0, 0, 3) - cam.getHeadOffset())
cam.setNearFarZ(0.001, 50)
cam.setEyeSeparation(0.0007)
cam.setBackgroundColor(Color(0,0,0,0))

geo = GeometryFile()
geo.loadModel(fileToLoad, textured=True)

handler = DAEventHandler()
handler.addGeo(geo)
setEventFunction(handler.onEvent)
setUpdateFunction(handler.onUpdate)
