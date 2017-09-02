import urllib2
import urllib
import sys


def sendTask(url, times):
	template = "http://localhost:8082/task?url=%s&times=%d"
	url_par = urllib.quote(url)
	times_par = int(times)
	url = template%(url_par,times_par)
	#print url
	response = urllib2.urlopen(url)
	response_contents = response.read()
	print response_contents
	print ""


def sendTaskFromFile(file_name):
	f = open(file_name)
	for line in f:
		url = line.split(':')[0]
		sendTask('https://www.whatsmydns.net/#A/'+url,3)
sendTask('https://www.whatsmydns.net/#A/google.com',3)
#sendTaskFromFile(sys.argv[1])
