# twrt-dump
tfw you don't want to go through 6000+ rts to save waifu images

----

requires:

python 2.7.x (maybe it works with 3.x, idk lol)

----

usage:
  1. login to twitter and navigate to https://twitter.com/settings/account
  2. scroll down to the content section and export your tweet history
  3. download and extract the folder into somewhere easy to access
  4. place my shitty script in the folder root
  5. open cmd and run "save.py mk" to generate a .csv list of urls
  6. afterwards, run "save.py dl" to start downloading the images
  7. let it run in the background and check back once in a while to see if it errors out lol

----

notes:

it will automatically append ":orig" to the end of each url before downloading for max waifures
  
dl is throttled to 8 second sleeps after every image, you can lower it if you want i guess

it will not attempt to redl files that already exist,
so make sure to delete bad/incomplete files before restarting it again after an error
  
this code is fucking terrible btw
