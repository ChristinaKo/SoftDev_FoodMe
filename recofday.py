import urllib2
import json
import random
from bs4 import BeautifulSoup
url = "http://food2fork.com/api/search?key=935a5bc621fcb061d17b50ef48278d1d&q=%s&page=%s"
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
        ran = random.randint(0,d['count']-1)
        if (d['recipes'][ran]['publisher']== "All Recipes"):
            return d['recipes'][ran]
        else:
            return rand()['source_url']
print rand()

