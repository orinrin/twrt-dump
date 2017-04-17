import os
import sys
import glob
import json
import time
import requests

listfile = "save.csv"
imagedir = "save.out"

try: sys.argv[1]
except: sys.argv.append(0)

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
				headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
				
				for url in urls:
					url = url.strip().split(",")[-1]
					dest = imagedir + os.sep + url.split("/")[-1]
					
					if url == "": continue
					if os.path.isfile(dest): continue
					
					print url
					
					with open(dest, "wb") as handle:
						response = session.get(url + ":orig", headers = headers, stream = True)
						time.sleep(8)
						
						for block in response.iter_content(1024): handle.write(block)
	else: print "no list found"
else: print "invalid arg"
