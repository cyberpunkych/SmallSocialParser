#!/usr/bin/python

from instagram.client import InstagramAPI
import sys
import re
import requests
from datetime import date
import time
import codecs
import urllib


api = InstagramAPI(client_id='', client_secret='')

map_html="""
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <script src="http://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>
    <script type="text/javascript">
        ymaps.ready(init);
        var myMap, 
            myPlacemark;

        function init(){ 
            myMap = new ymaps.Map("map", {
                center: [55.76, 37.64],
                zoom: 5
            }); 
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
map_html1=""

while count_media<int(photos_len[0]):
	for i in recent_media[0]:
		try:
			if i.location:
				pass
				print "======================="
				print i.link
				print i.location

				map_html1+=u"myPlacemark = new ymaps.Placemark(["+str(i.location.point.latitude)+", "+str(i.location.point.longitude)+"], {\n"
				
				if i.location.id=='0':
					map_html1+=u" hintContent: ' ',\n balloonContent: decodeURIComponent('<a target=\"_blank\" href=\"{}\">{}</a><br><img src=\"{}\">') }}, {{ preset: 'islands#dotIcon' }} );\n myMap.geoObjects.add(myPlacemark);\n\n".format(i.link, i.link, i.images["low_resolution"].url)	
				else:
					map_html1+=u" hintContent: ' ',\n balloonContent: decodeURIComponent('<a target=\"_blank\" href=\"{}\">{}</a><br><img src=\"{}\">') }} );\n myMap.geoObjects.add(myPlacemark);\n\n".format(i.link, i.link, i.images["low_resolution"].url)	



		except Exception as error:
			pass
			#print error

	if recent_media[0] == []:
		pass
	else:
		last_id=str(recent_media[0][-1]).split(' ')[1]
		recent_media = api.user_recent_media(user_id=str(user_id), max_id=last_id)
		count_media = count_media + len(recent_media[0])


map_html+=map_html1

map_html+="""




  }
    </script>
</head>

<body>
    <div id="map" style="width: 600px; height: 400px"></div>
</body>

</html>
"""

map_file=codecs.open(sys.argv[1]+'_'+str(date.today().year)+'_'+str(date.today().month)+'_'+str(date.today().day)+'.html', 'w', "utf-8")
map_file.write(map_html)
map_file.close

print "======================="
