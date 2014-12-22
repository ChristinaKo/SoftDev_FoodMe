import urllib2
import json
#edamam

plus="%2C+"

#http://docs.python-requests.org/en/latest/index.html

url="""
https://api.edamam.com/api/nutrient-info?
"""

request = urllib2.urlopen(url)
result = request.read()
print result

print "asdklfjasdklfjklasd;fjkl;asdfj\n\n\n\n\n\n\n\n\n\n\n\n"
d = json.loads(result)
print d
if len(d['results']) > 0:
    print "items found"

