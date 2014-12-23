import urllib2
import json
#edamam

plus="%2C+"


#edamam has weird http errors- no authorization issues. TRY Nutritionix
#urllib2.HTTPError: HTTP Error 401: Unauthorize
#http://docs.python-requests.org/en/latest/index.html

base = "http://api.edamam.com/api/nutrient-info?extractOnly&url=http:http://allrecipes.com/Recipe/Albondigas&api_id=&api_key="
print base
request = urllib2.urlopen(base)
result = request.read()
print result

d = json.loads(result)
print d
if len(d['results']) > 0:
    print "items found"

