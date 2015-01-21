import urllib2
import json
from bs4 import BeautifulSoup
import nutrition
url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=chicken%20nuggets"
request = urllib2.urlopen(url)
result = request.read()
d = json.loads(result)
rurl= ""
irl= ""
ingredients=[]
recipe=[] #actual recipe
recipes=[] #list of many different recipes
##THis is to find Recipes with all recipes url.
def getrecipes():
    for r in d['recipes']:
        if r['publisher']== "All Recipes":
            recipes.append([r['title'],r['source_url'],r['f2f_url']])
            # title = name of the recipe
            # source_url = allrecipes url
            # f2f_url = food 2 fork url
     return recipes       
print getrecipes
    

def retrecipe(iurl):
    res = urllib2.Request(rurl) ##rurl is surl[1] or whatever link is chosen 
    x = u
    rllib2.urlopen(res)
    html = x.read()
    html =BeautifulSoup(html)
    for i in  html.find_all("span"):
        if i.get('class') == ['plaincharacterwrap', 'break']:
            recipe.append(i.get_text())
    return recipe
            ############print recipe
##ingredients
def reting(iurl):
    res = urllib2.Request(iurl)#corresponding f2f url so if rurl = surl[1] then iurl=furl[1]
    x = urllib2.urlopen(res)
    html = x.read()
    html = BeautifulSoup(html)
    for i in html.find_all("li",itemprop="ingredients"):
        ingredients.append(i.get_text())
    return ingredients    
print reting(recipes[0][2])
print nutrition.parser(ingredients)
# [u' 3 skinless, boneless chicken breasts', u' 1 cup Italian seasoned bread crumbs', u' 1/2 cup grated Parmesan cheese', u' 1 teaspoon salt', u' 1 teaspoon dried thyme', u' 1 tablespoon dried basil', u' 1/2 cup butter, melted']  --> LISE this is how it should look when it is in the array for "chicken nuggets"
