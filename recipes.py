from flask import Flask,request,url_for,redirect,render_template
import urllib2
import json
app=Flask(__name__)
url = "http://food2fork.com/api/search?key=64e7c9ab4a5b566ec0aee5ea832f1ee2&q=mozzarella%20sticks"
request = urllib2.urlopen(url)
result = request.read()
#print result
d = json.loads(result)
#print d
surl= ""
@app.route("/")
def returnRecipeURL():
    page = ""
    rurl= ""
    for r in d['recipes']:
        for i in r['source_url']:
            rurl = rurl + i
    return  rurl
@app.route("/allr")
def returnallrecipe():
    page = ""
    rurl= ""
    for r in d['recipes']:
        if r['source_url'].find("allrecipes") != -1:
            surl= r['source_url']
        return surl
@app.route("/recipe")
def returnRecipe():
    page = ""
    rurl= ""
    for r in d['recipes']:
        if r['source_url'].find("allrecipes") != -1:
            surl= r['source_url']
    res = urllib2.Request(surl) ##take in the source url from previous method
    x = urllib2.urlopen(res)
    html = x.read()
    splitr = html.split("<ol>")
    splitr = splitr[1].split("</ol>")
    return "Directions:<br><ol>" + splitr[0] + "</ol>"
if __name__=="__main__":
    app.debug=True
    app.run(host="0.0.0.0",port=5000)
