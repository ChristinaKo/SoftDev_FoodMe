import urllib2
import json
from bs4 import BeautifulSoup
url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=chicken%20nuggets"
request = urllib2.urlopen(url)
result = request.read()
d = json.loads(result)
surl= ""
rurl= ""
furl=""
ingredients=[]
for r in d['recipes']:
    for i in r['source_url']:
        rurl = rurl + i
#print rurl ## prints recipe url 

for r in d['recipes']:
    if r['source_url'].find("allrecipes") != -1:
        surl= r['source_url']
#print surl #prints recipe url of allrecipes (As of now)

# for r in d['recipes']:
#     if r['source_url'].find("allrecipes") != -1:
#         surl= r['source_url']
# res = urllib2.Request(surl) ##take in the source url from previous method
# x = urllib2.urlopen(res)
# html = x.read()
# html =BeautifulSoup(html)
#print html.find(itemprop="ingredients")
#print html.prettify()
#print html.get_text()
# splitr = html.split("<ol>")
# splitr = splitr[1].split("</ol>")
# print "Directions:<br><ol>" + splitr[0] + "</ol>" #prints the recipe of ...

##ingredients
for r in d['recipes']:
    if r['source_url'].find("allrecipes") != -1:
        furl= r['f2f_url']
res = urllib2.Request(furl) ##take in the source url from previous method
x = urllib2.urlopen(res)
html = x.read()
html = BeautifulSoup(html)
for i in html.find_all("li",itemprop="ingredients"):
        ingredients.append(i.get_text())
print ingredients

# [u' 4 skinless, boneless chicken breasts', u' 2 cups corn oil', u' 1 egg, beaten', u' 1/3 cup water', u' 1/3 cup all-purpose flour', u' 1 1/2 tablespoons sesame seeds, toasted', u' 1 1/2 teaspoons salt']  --> LISE this is how it should look when it is in the array for "chicken nuggets"
