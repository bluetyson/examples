from webView import *

#width = 11020
#height = 1200
width = 1200
height = 800

ww = None

ui = UiModule.createAndInitialize()
uiroot = ui.getUi()

if(isMaster()):
	ww = WebView.create(width, height)
	ww.loadUrl("file:///local/examples/parallel/weather/index.htm")
	frame = WebFrame.create(uiroot)
	frame.setView(ww)
else:
	ww = PixelData.create(width, height, PixelFormat.FormatRgba)
	frame = Image.create(uiroot)
	frame.setDestRect(250,0,11020, 1200)
	frame.setData(ww)

ImageBroadcastModule.instance().addChannel(ww, "webpage", ImageFormat.FormatNone)