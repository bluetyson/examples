from webView import WebView, WebFrame
from euclid import Vector2, Vector3
from omega import SceneNode, getDefaultCamera, getEvent, ServiceType

width = 1448
height = 1000


cam = getDefaultCamera()
cam.setEyeSeparation(0)

ww = None

ui = UiModule.createAndInitialize()

cont = Container.create(ContainerLayout.LayoutFree, ui.getUi())

myNode = SceneNode.create("myNode")

c3d = cont.get3dSettings()
c3d.enable3d = True
c3d.position = Vector3(-2, 2.5, -4) # orig
c3d.scale = 0.001
c3d.node = myNode

ww = WebView.create(width, height)
#ww.setZoom(200)
ww.loadUrl("file:///local/examples/parallel/University/CompetitiveGrantsIncome/Commonwealth/index.html")
frame = WebFrame.create(cont)
frame.setView(ww)


cont2 = Container.create(ContainerLayout.LayoutFree, ui.getUi())

myNode2 = SceneNode.create("myNode2")

c3d = cont2.get3dSettings()
c3d.enable3d = True
c3d.position = Vector3(-0.5, 2.5, -4) # orig
c3d.scale = 0.001
c3d.node = myNode2

ww = WebView.create(width, height)
#ww.setZoom(200)
ww.loadUrl("file:///local/examples/parallel/University/CompetitiveGrantsIncome/Total/index.html")
frame = WebFrame.create(cont2)
frame.setView(ww)



cont3 = Container.create(ContainerLayout.LayoutFree, ui.getUi())

myNode3 = SceneNode.create("myNode3")

c3d = cont3.get3dSettings()
c3d.enable3d = True
c3d.position = Vector3(1, 2.5, -4) # orig
c3d.scale = 0.001
c3d.node = myNode3

ww = WebView.create(width, height)
#ww.setZoom(200)
ww.loadUrl("file:///local/examples/parallel/University/CompetitiveGrantsIncome/NonCommonwealth/index.html")
frame = WebFrame.create(cont3)
frame.setView(ww)

ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatNone)

cursorImg = loadImage('/da/sw/omegalib/myCursor.png')
cursorClickImg = loadImage('/da/sw/omegalib/myCursor_click.png')
currentUser = 0

cursors = []
labels = []

names = [
	"Glenn", # name of person controlling
	"Darren",
	"Ben",
	"Marcus",
	"Hugh",
]
cols = [
	'#FF0000',
	'#00FF00',
	'#0000FF',
	'#FFFF00',
	'#00FFFF',
]

for i in range(5):
	cursor = Image.create(cont)
	label = Label.create(cont)
	label.setText(names[i])
	label.setFont('fonts/arial.ttf 18')
	label.setColor(Color('white'))
	label.setPosition(Vector2(32, 12))
	label.setFillEnabled(True)
	label.setFillColor(Color(cols[i]))

	if i == 0:
		cursor.setSize(Vector2(32, 32))
		cursor.setData(cursorImg)
	else:
		cursor.setData(loadImage('/da/sw/omegalib/myCursor_' + str(i + 1) + '.png'))
		cursor.setSize(Vector2(24, 24))
	cursors.append(cursor)
	labels.append(label)

prevOrientations = [[Quaternion()]] * len(names)

prevDiffAmt = 0.0

def diff(q1, q2):
	return ((abs(q2.w) + abs(q2.x) + abs(q2.y) + abs(q2.z)) -
		 (abs(q1.w) + abs(q1.x) + abs(q1.y) + abs(q1.z)))

def onEvent():

	global currentUser, cursors, labels
	global cursorClickImg, cursorImg
	global prevOrientations, prevDiffAmt

	e = getEvent()

	if e.getServiceType() == ServiceType.Mocap:
		if e.getExtraDataItems() >= 2:
			point = Vector2(e.getExtraDataInt(0), e.getExtraDataInt(1))
			if e.getUserId() > len(cursors):
				return

			#po = prevOrientations[e.getUserId() - 1]
			po = Quaternion()

			for a in prevOrientations[e.getUserId() - 1]:
				#a.w *= (1.0 / len(prevOrientations[e.getUserId() - 1]))
				#po *= a
				po.w += a.w
				po.x += a.x
				po.y += a.y
				po.z += a.z

			po.w /= 1.0 * len(prevOrientations[e.getUserId() - 1])
			po.x /= 1.0 * len(prevOrientations[e.getUserId() - 1])
			po.y /= 1.0 * len(prevOrientations[e.getUserId() - 1])
			po.z /= 1.0 * len(prevOrientations[e.getUserId() - 1])

			aa = e.getOrientation()
			diffAmt = diff(aa, po)

			diffChange = abs(diffAmt - prevDiffAmt)

			# TODO use change in diff from average of previous quats to compare against
			if diffChange < 0.075:
				print "diff change:", diffChange
				cursors[e.getUserId() - 1].setPosition(point)
				labels[e.getUserId() - 1].setPosition(point + Vector2(32, 12))

			prevDiffAmt = diffAmt

			prevOrientations[e.getUserId() - 1].append(e.getOrientation())
			if len(prevOrientations[e.getUserId() - 1]) >= 4:
				prevOrientations[e.getUserId() - 1].pop(0)

		if (e.getUserId() == 1):
			vec = e.getOrientation() * Vector3(0, 1, 0)

			if vec[1] < -0.6:
				cursors[e.getUserId() - 1].setData(cursorClickImg)
			else:
				cursors[e.getUserId() - 1].setData(cursorImg)

setEventFunction(onEvent)
