import xbmc
import xbmcaddon
import json
import os
import sys

# Add our resources/lib to the python path
try:
   current_dir = os.path.dirname(os.path.abspath(__file__))
except:
   current_dir = os.getcwd()

sys.path.append(os.path.join(current_dir, 'resources', 'lib'))

from sseclient import SSEClient

__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

deviceID = __addon__.getSetting( "deviceid" )
accessToken = __addon__.getSetting( "accesstoken" )
time = (int(__addon__.getSetting( "time" )) * 1000)  #in miliseconds

xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Spark service','Started service', 1000, __icon__))

messages = SSEClient('https://api.spark.io/v1/devices/' + deviceID + '/events/?access_token=' + accessToken)

my_string = __addon__.getSetting( "keywords" )
my_list = my_string.split(",")


for msg in messages:
	if(xbmc.abortRequested):break
	if my_string:
		for key in my_list:
			if key in msg.event:
				decoded = json.loads(msg.data)
				message = decoded['data']
				header = msg.event
				xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(header,message, time, __icon__))
	else:
		if msg.data:
			decoded = json.loads(msg.data)
			message = decoded['data']
			header = msg.event
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(header,message, time, __icon__))

