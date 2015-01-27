from flask import Flask, render_template, request
import urllib2
import json
from nutritionix import Nutritionix

##################### Flask Header ############################
app = Flask(__name__)
app.secret_key = "SEcRet KeY"
###################KEY INFO HERE FOR API ACCESS#################################
#you need to place an API key for Nutritionix here - provide one here below
#nx = Nutritionix (api_key = "daee2f4c8cc606f01466792b71d9a431", app_id = "1634d1d7")
### this is the second api key cuz, the first got overused
nx = Nutritionix(app_id="3df3337e", api_key="cff8d58ebc11131a0cd7f28a5432a60f")
################################################################################

####### Helper Functions #######
#compares the item-name to find measurement words
def compare(item, measureu):
    plural = measureu + "s"
    temp = item["fields"]["item_name"].split()
    if measureu in temp or plural in temp:
        return True
    return False

#returns amount from Nutritionix database
def amountfind (item, measureu):
    temp = item["fields"]["item_name"].split()
    if measureu in temp:
        try:
            return float(temp[temp.index(measureu)-1])
        except:
            print "Amountfind - ARRAY ERROR"
    return float(item["fields"]["nf_serving_size_qty"])
        
##Scales nutrition facts and combines with the passed original info
def scale (dic, factor, orig):
    ans = {}
    x = dic.keys()
    for key in x:
        if dic[key] != None:
            ans[key] = dic[key]*factor
        else: #if not num / == None, then skip
            pass
        if len(orig) > 0: #if something in orig
            try:
                ans[key] = orig[key] + ans[key]
            except: #if not orig key should i make a new one or something, or pass?? ******
                pass            
    return ans
            
#checks to see no extraneous measurement words that will mess up search
def check(measurement):
    L = ["cup", "teaspoon", "tablespoon", "quart", "pint", "pound", "lb", "ounce",
        "cups", "teaspoons", "tablespoons", "quarts", "pints", "pounds", "lbs", "ounces", "oz"]
    return measurement in L

def clean (L):
    dump =["of"]
    for x in L:
        if x in dump:
            L.remove(x)
    return " ".join(L)

def fractioncheck(x):
    if x.find("/") == -1:
        return x
    else:
        z = x.split('/')
        return float(z[0])/float(z[1])

def nformat(dic, s, dv = None):
    percent = 100
    if dv == None:
        dv = 1
        percent = 1
    if s in dic.keys():
        print s
        print dic[s]
        print dv
        print percent
        return int(dic[s]*percent/dv)
    return 0

############################### API CALL FUNCTIONS #######################################
#'''''''''''''''''''''''''''''''''''''''''SEARCHING''''''''''''''''''''''''''''''''''''''''''''''''''''#

#returns one result of a search of params (using amounts and measurements as qualifiers)
def search(param, amount, measurement):
    lists=[] # list of one element id
    request = nx.search(param,limit=100, offset=0, search_type="usda")
    result = request.json()
    if result["total_hits"] >0:
        for item in result["hits"]: #is result hits top 10
            if (item["fields"]["nf_serving_size_unit"] == measurement or item["fields"]["nf_serving_size_unit"] == measurement+"s" or compare(item, measurement)):
                lists.append(item["fields"]["item_id"])
                lists.append(measurement)
                lists.append(amountfind(item,measurement))
                return lists   # list of one element
        item = result["hits"][0]
        lists.append(item["fields"]["item_id"])
        lists.append(measurement)
        lists.append(amountfind(item,measurement))
        return lists
            
#parses through list of item_ids and searches for nutrition facts     
def getAstats(item_id):
    allergen= ["allergen_contains_eggs","allergen_contains_fish","allergen_contains_gluten","allergen_contains_milk","allergen_contains_peanuts","allergen_contains_shellfish","allergen_contains_tree_nuts","allergen_contains_wheat", "allergen_contains_soybeans"]
    nutrifacts= nx.item(id=item_id).json()
    LT = [] #List of allergens
    for n in allergen:
        try:
            if nutrifacts[n] != None:
                LT.append(n[18:])
        except:
            print n + "  ___   key DNE in this set"
            
    NF = ["nf_calories","nf_calories_from_fat","nf_total_fat","nf_saturated_fat","nf_trans_fatty_acid","nf_cholesterol","nf_sodium","nf_total_carbohydrate","nf_dietary_fiber","nf_sugars","nf_protein","nf_vitamin_a_dv","nf_vitamin_c_dv","nf_calcium_dv","nf_iron_dv"]
    fact = {}
    for f in NF:
        try:
            fact[f] = nutrifacts[f]
        except:
            print "key error: " + f
    return [fact, LT]

#''''''''''''''''''''''''''''''''''''''''''' Main Function  ''''''''''''''''''''''''''''''''''''#
################################Parses and then searches########################
#parses through list of ingredients from food to fork and finds all nutrition facts
def parser(ingredlist):
    searchL = []
    allergens = []
    nutri= {}
    #setting up for searching
    for i in ingredlist:
        ingred = i.strip() 
    #start of parsing stuff
        x = ingred.split()
       #ASSUMING that amount is the first element of this split list
        
        if x[0] == "a":
            f2famount = float(1.0)
        else:
            f2famount= float(fractioncheck(x[0]))
        x.pop(0) #popping the amount 
        if check(x[0]):
            measurement = x[0]
            x.pop(0)
            searchL = clean(x)
        else:
            measurement="serving"
            searchL = clean(x)
    #search using the search params
        results = search(searchL, f2famount, measurement)
        resultid = results[0] #Nutritionix id of the search element
        measurement = results[1] #measurement used by the id which has been checked with measurement used in the passed recipe
        amount = results[2] #amount from Nutritionix database
        scalefactor = 1.0*amount/f2famount 
    #get nutri/allergen facts
        stats = getAstats(resultid)  #list of nutri facts, allergens
        #combine
        nutri = scale(stats[0], scalefactor, nutri)
        allergens = list(set(stats[1]+allergens)) #double-check this to see if it removes duplicates
    return [nutri, allergens, measurement]
    #return searchL #we dont need to return the search Lists

############################FLASK COMMANDS################################
# this should go into the search engine part..... im using another html file just just test this out
@app.route("/nutrition")
def run():
######################## This should be replaced with the actual input from f2f
    source = ["1/2 cup grated Parmesan cheese", "1 teaspoon salt", "1 teaspoon dried thyme", "1 tablespoon dried basil", "1/2 cup butter, melted"]
###########################
    nutrifact = parser(source)
    n = nutrifact[0]
    allergen= nutrifact[1]
    return render_template("n.html",
                           sizes = "1 meal",
                           serverpcont = "1" ,
                           calories = nformat(n,"nf_calories"),
                           fatcals = nformat(n,"nf_calories_from_fat"),
                           fat = nformat(n,"nf_total_fat"), 
                           fatdv = nformat(n,"nf_total_fat",65), 
                           satfat = nformat(n,"nf_saturated_fat"), 
                           satfatdv = nformat(n,"nf_saturated_fat",20),
                           transfat = nformat(n,"nf_trans_fatty_acid"),
                           cholesterol = nformat(n,"nf_cholesterol"),
                           cholesteroldv = nformat(n,"nf_cholesterol",300),
                           sodium = nformat(n,"nf_sodium"),
                           sodiumdv = nformat(n,"nf_sodium",2400),
                           carb = nformat(n,"nf_total_carbohydrate"), 
                           carbdv = nformat(n,"nf_total_carbohydrate",300), 
                           df = nformat(n,"nf_dietary_fiber"), 
                           sugar = nformat(n,"nf_sugars"),
                           protein = nformat(n,"nf_protein"),
                           proteindv = nformat(n,"nf_protein",50),
                           vitA = nformat(n,"nf_vitamin_a_dv"),
                           vitC = nformat(n,"nf_vitamin_a_dv"),
                           calcium = nformat(n,"nf_calcium_dv"),
                           iron= nformat(n,"nf_iron_dv"),
                           allergens = allergen
                           )

##########################################################################
############Testing Section
if __name__ == "__main__":
    app.debug = True
    app.run()
