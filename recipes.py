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
recipe=[]
for r in d['recipes']:
    if r['publisher']== "All Recipes":
        surl= r['source_url']
        furl= r['f2f_url']
        break
    
res = urllib2.Request(surl) ##take in the source url from previous method
x = urllib2.urlopen(res)
html = x.read()
html =BeautifulSoup(html)
for i in  html.find_all("span"):
    if i.get('class') == ['plaincharacterwrap', 'break']:
        recipe.append(i.get_text())
print recipe

##ingredients

res = urllib2.Request(furl) ##take in the source url from previous method
x = urllib2.urlopen(res)
html = x.read()
html = BeautifulSoup(html)
for i in html.find_all("li",itemprop="ingredients"):
    ingredients.append(i.get_text())
print ingredients

# [u' 3 skinless, boneless chicken breasts', u' 1 cup Italian seasoned bread crumbs', u' 1/2 cup grated Parmesan cheese', u' 1 teaspoon salt', u' 1 teaspoon dried thyme', u' 1 tablespoon dried basil', u' 1/2 cup butter, melted']  --> LISE this is how it should look when it is in the array for "chicken nuggets"
