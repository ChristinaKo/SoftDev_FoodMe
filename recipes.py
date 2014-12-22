from flask import Flask,request,url_for,redirect,render_template
import urllib2
import json

url = "http://food2fork.com/api/search?key={SECRET KEY')"
request = urllib2.urlopen(url)
result = request.read()
print result

d = json.loads(result)
