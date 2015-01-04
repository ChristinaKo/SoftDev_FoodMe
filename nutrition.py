import urllib2
import json
from nutritionix import Nutritionix
###################KEY INFO HERE FOR API ACCESS##################################

nx = Nutritionix (api_key = "",
                  api_id = "")

################################################################################

request = nx.search("cheese")
result = request.json()
#edamam has weird http errors- no authorization issues. TRY Nutritionix
#Food4Me
#https://github.com/leetrout/python-nutritionix
#urllib2.HTTPError: HTTP Error 401: Unauthorize
#http://docs.python-requests.org/en/latest/index.html
#edamam

''''
plus="%2C+"
base = "http://api.edamam.com/api/nutrient-info?extractOnly&url=http:http://allrecipes.com/Recipe/Albondigas&api_id=&api_key="
print base
request = urllib2.urlopen(base)
result = request.read()
print result
#d = json.loads(result)
'''
################################################################################
def search(param):
    request = nx.search("cheese")
    result = request.json()
    d = result
    if len(d) > 0:
        print "items found"
    print d

