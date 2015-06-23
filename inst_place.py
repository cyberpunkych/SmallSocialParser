#!/usr/bin/python

from instagram.client import InstagramAPI
import sys
import re
import requests

api = InstagramAPI(client_id='4412fd0dc9f04234bc7ed93a85463502', client_secret='e155859592c84346ab775f4d0b0e000e')

r=requests.get("https://instagram.com/"+str(sys.argv[1])+"/")
html=r.text

user_id = int(re.findall('<meta property="og:image" content="([^>]+)" />', html)[0].split('_')[1])
photos_len = re.findall('"count":([^.]+),"page', html)

print "======================="
print "User id: "+str(user_id)
print "Count media: "+str(photos_len[0])


recent_media = api.user_recent_media(user_id=str(user_id), count=33)

count_media=len(recent_media[0])

while count_media<=photos_len:
	try:
		#print count_media
		for i in recent_media[0]:
			try:
				if i.location:
					print i.link
					print i.location
			except Exception:
				pass
		last_id=recent_media[0][len(recent_media[0])-1]
		last_id=last_id.caption.id+"_"+last_id.caption.user.id
		recent_media = api.user_recent_media(user_id=str(user_id), count=33, min_id=last_id)
		count_media = count_media + len(recent_media[0])
	except Exception:
		pass


#recent_media = api.user_recent_media(user_id=str(user_id), count=int(sys.argv[2]))

def get_media(medias):
	for i in medias[0]:
		#print i #debug
		try:
			if i.location:
				print "======================="
				print i.link
				print i.location
				
		except Exception:
			pass
		print "======================="   	

#print api.media(media_id=str(sys.argv[1])).location