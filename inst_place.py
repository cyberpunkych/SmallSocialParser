#!/usr/bin/python

from instagram.client import InstagramAPI
import sys
import re
import requests
from datetime import date
import time
import codecs
import urllib


api = InstagramAPI(client_id='4412fd0dc9f04234bc7ed93a85463502', client_secret='e155859592c84346ab775f4d0b0e000e')

map_html=u"""
<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <script src="http://api-maps.yandex.ru/1.1/index.xml" type="text/javascript"></script>
    </head>
    <body>            
            <div id="YMapsID" style="position: fixed;top: 0;left: 0;width: 100%;height: 100%;"></div>
            <script type="text/javascript">
  YMaps.jQuery(function () {

        var map = new YMaps.Map(YMaps.jQuery("#YMapsID")[0]);
            





map.addControl(new YMaps.TypeControl());
map.addControl(new YMaps.ToolBar());
map.addControl(new YMaps.Zoom());
map.addControl(new YMaps.MiniMap());
map.addControl(new YMaps.ScaleLine());

 map.setCenter(new YMaps.GeoPoint(37.64, 55.76), 3);

"""


r=requests.post("http://www.otzberg.net/iguserid/index.php", data={"q":str(sys.argv[1]), "mode":"getid"})
html=r.text

print "======================="

try:
	user_id = int(re.findall('<h4>([^>]+)</h4>', html)[1].split(' ')[2])

	r1=requests.get("https://instagram.com/"+sys.argv[1]+"/")
	photos_len = re.findall('"count":([^.]+),"page', r1.text)
except Exception, e:
	print "Bad username! Exit..."
	print "======================="   	
	exit()





print "User id: "+str(user_id)
try:
	print "Count media: "+str(photos_len[0])
except Exception:
	print "Profile is privat!"
	print "======================="
	exit()

recent_media = api.user_recent_media(user_id=str(user_id))
count_media=len(recent_media[0])

last_id=0

while count_media<int(photos_len[0]):
	for i in recent_media[0]:
		try:
			if i.location:
				pass
				print "======================="
				print i.link
				print i.location
#				print i.caption
				
				
				if i.location.id=='0':
					map_html+=u"var placemark = new YMaps.Placemark(new YMaps.GeoPoint("+str(i.location.point.longitude)+", "+str(i.location.point.latitude)+"), {style: \"default#greenPoint\"}, {hideIcon: false});\n"
				else:
					map_html+=u"var placemark = new YMaps.Placemark(new YMaps.GeoPoint("+str(i.location.point.longitude)+", "+str(i.location.point.latitude)+"), {hideIcon: false});\n"
				
				map_html+=u"placemark.name = \"<a target='_blank' href='{}'>{}</a>\";\n placemark.description = decodeURIComponent('<img src=\"{}\">');\n map.addOverlay(placemark);\n\n".format(i.link, i.link, i.images["low_resolution"].url)
				 


		except Exception as error:
			pass
			#print error

	if recent_media[0] == []:
		pass
	else:
		last_id=str(recent_media[0][-1]).split(' ')[1]
		recent_media = api.user_recent_media(user_id=str(user_id), max_id=last_id)
		count_media = count_media + len(recent_media[0])


map_html+=u"""





    })

            </script>
        </div>
    </body>
</html>
"""

file_name=sys.argv[1]+'_'+str(date.today().year)+'_'+str(date.today().month)+'_'+str(date.today().day)+'.html'
map_file=codecs.open(file_name, 'w', "utf-16")
map_file.write(map_html)
map_file.close


print "\n======================="
print "Open "+sys.argv[1]+'_'+str(date.today().year)+'_'+str(date.today().month)+'_'+str(date.today().day)+'.html'+" in your browser"
print "======================="
