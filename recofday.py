import urllib2
import json
import random
from bs4 import BeautifulSoup
url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=%s&page=%s"
def rand():
    randletter = random.choice("abcdefghijklmnopqrstuvwxyz")
    randnum = random.randint(0,100)
    nurl = url%(randletter, randnum)
    request = urllib2.urlopen(nurl)
    result = request.read()
    d = json.loads(result)
    if d['count'] == 0:
        return rand()
    else:
        return d['recipes'][random.randint(0,d['count'])]
print rand()

