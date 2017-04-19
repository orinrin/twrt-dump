import os
import sys
import glob
import json
import time
import requests

listfile = "save.csv"
imagedir = "save.out"

username = "YourHandle"
likefile = "like.csv"

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

try: sys.argv[1]
except: sys.argv.append(0)

if sys.argv[1] == "ldl":
	sys.argv[1] = "dl"
	listfile = likefile

if sys.argv[1] == "mk":
	with open(listfile, "wb") as list:
		list.write("User,TweetURL,MediaURL\r\n")
		
		files = glob.glob("data/js/tweets/*.js")
		
		for file in reversed(files):
			with open(file, "rb") as data:
				tweets = json.loads("".join(data.readlines()[1:]))
				
				for tweet in tweets:
					try: user = "@" + tweet["retweeted_status"]["user"]["screen_name"]
					except: continue
					
					pics = tweet["entities"]["media"]
					
					if len(pics) < 1:
						try: pics = tweet["retweeted_status"]["entities"]["media"]
						except: pics = []
					
					for pic in pics:
						exp = pic["expanded_url"]
						url = pic["media_url_https"]
						
						if url.find("/media/") < 0: continue
						
						list.write("{},{},{}\r\n".format(user, exp, url))

elif sys.argv[1] == "dl":
	if os.path.isfile(listfile):
		if not os.path.isdir(imagedir): os.mkdir(imagedir)
		
		with open(listfile, "rb") as list:
			urls = list.read().split("\r\n")[1:]
			
			with requests.Session() as session:
				for url in urls:
					url = url.strip().split(",")[-1]
					dest = imagedir + os.sep + url.split("/")[-1]
					
					if url == "": continue
					if os.path.isfile(dest): continue
					
					print url
					
					with open(dest, "wb") as handle:
						fail = 0
						
						while fail < 3:
							try:
								response = session.get(url + ":orig", headers = headers, stream = True)
								time.sleep(8)
								break
							except:
								fail += 1
								time.sleep(16)
						
						if fail > 2: print "unable to retrieve image"; quit()
						
						for block in response.iter_content(1024): handle.write(block)
	
	else: print "no list found"

elif sys.argv[1] == "lmk":
	import urllib
	
	from bs4 import BeautifulSoup
	
	with open(likefile, "wb") as list:
		list.write("User,TweetURL,MediaURL\r\n")
		
		with requests.Session() as session:
			ids = []
			last = -1
			
			while last != 0:
				# bypass the developer api entirely using widget calls, likely to break in the future
				if last < 0: request = "https://cdn.syndication.twimg.com/timeline/likes?callback=__twttr.callbacks.tl_i1_likes_{0}_old&lang=en&screen_name={0}&suppress_response_codes=true".format(username)
				else: request = "https://cdn.syndication.twimg.com/timeline/likes?callback=__twttr.callbacks.tl_i1_likes_{0}_old&lang=en&max_position={1}&screen_name={0}&suppress_response_codes=true".format(username, last)
				
				print request
				
				last = 0
				fail = 0
				
				while fail < 3:
					try:
						response = session.get(request, headers = headers)
						time.sleep(8)
						break
					except:
						fail += 1
						time.sleep(16)
				
				if fail > 2: print "unable to retrieve timeline"; quit()
				
				# no idea what response is sent when i reach an invalid timeline, but im pretty sure its not going to have an html body lol
				try: soup = BeautifulSoup(json.loads(response.text.split("(", 1)[-1].rsplit(")", 1)[0])["body"], "html.parser")
				except: break
				
				tweets = soup.findAll("div", {"data-scribe" : "component:tweet"})
				
				if len(tweets) < 1: break
				
				for tweet in tweets:
					last = tweet["data-tweet-id"]
					
					if last in ids: last = 0; break
					
					ids.append(last)
					
					user = tweet.find("span", {"data-scribe" : "element:screen_name"})["title"]
					
					# STUPID WORKAROUND FOR TWEETS WITH MULTIPLE IMAGES THAT RELIES ON A LOCALE SPECIFIC STRING
					pics = tweet.findAll("img", {"title" : "View image on Twitter"})
					
					for pic in pics:
						exp = pic.parent["href"]
						
						try: url = urllib.unquote(pic["data-srcset"]).split(" ")[0].split(":small")[0].split(":large")[0].split(":orig")[0]
						except: continue
						
						list.write("{},{},{}\r\n".format(user, exp, url))

else: print "invalid arg"
