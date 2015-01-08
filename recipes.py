import urllib2
import json
from bs4 import BeautifulSoup
url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=mozzarella%20sticks"
request = urllib2.urlopen(url)
result = request.read()
d = json.loads(result)
#print d
surl= ""
page = ""
rurl= ""
furl=""

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
for i in html.find_all("span"):
    if i['class'] == "plaincharacterwrap break":
        print i.get_text()

# spliti = html.split("<ul>")
# spliti = spliti[1].split("</ul>")
# spliti=spliti[0].split("</li>")
# for i in spliti:
#     print i[26:]
    
# #Print  "Ingredients:<br><ul>" + spliti[0] + "</ul>"   
