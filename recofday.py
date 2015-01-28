import urllib2
import json
import random
from bs4 import BeautifulSoup

#Angela's key: 935a5bc621fcb061d17b50ef48278d1d
#Christina's key: 64e7c9ab4a5b566ec0aee5ea832f1ee2
#Key 3: 73fabb20981c227717084598dff04287
#Key #4:ea433f0fab9479fcdb2601ee80912e5c
#key 5:c6c725b11b322d241aea51a4038c990a

#url = "http://food2fork.com/api/search?key=73fabb20981c227717084598dff04287&q=%s&page=%s"
#url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=%s&page=%s"
#url = "http://food2fork.com/api/search?key=c6c725b11b322d241aea51a4038c990a&q=%s&page=%s"
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
            return rand()
#print rand()
