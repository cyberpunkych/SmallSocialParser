#!/usr/bin/python

from instagram.client import InstagramAPI
import sys
import re
import requests

api = InstagramAPI(client_id='4412fd0dc9f04234bc7ed93a85463502', client_secret='e155859592c84346ab775f4d0b0e000e')




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
				print i.caption
		except Exception:
			pass

	if recent_media[0] == []:
		pass
	else:
		last_id=str(recent_media[0][-1]).split(' ')[1]
		recent_media = api.user_recent_media(user_id=str(user_id), max_id=last_id)
		count_media = count_media + len(recent_media[0])

print "======================="