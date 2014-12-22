import urllib2
import json

plus="%2C+"



url="""
http://www.recipepuppy.com/api/?i=corn&q=&p=12123123
"""

#recipe puppy stuff

request = urllib2.urlopen(url)
result = request.read()
print result

print "asdklfjasdklfjklasd;fjkl;asdfj\n\n\n\n\n\n\n\n\n\n\n\n"
d = json.loads(result)
print d
if len(d['results']) > 0:
    print "items found"

