from flask import Flask, render_template, request
import urllib2
import json
import math
from nutritionix import Nutritionix

##################### Flask Header ############################
app = Flask(__name__)
app.secret_key = "SEcRet KeY"

###################KEY INFO HERE FOR API ACCESS#################################
#you need to place an API key for Nutritionix here - provide one here below
nx = Nutritionix (api_key = "c61a0fa95a3d990372245f601358afe3",
                  app_id = "1634d1d7")
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
            # print "{0:0.1f}".format(ans[key])
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
      
#print fractioncheck("1/2")
#print fractioncheck("12312")
        
###############################API CALL FUNCTION#######################################
#'''''''''''''''''''''''''''''''''''''''''SEARCHING''''''''''''''''''''''''''''''''''''''''''''''''''''#

#returns one result of a search of params (using amounts and measurements as qualifiers)
#checks measurement and amounts
def search(param, amount, measurement):
    print param
    print measurement
   
    lists=[] # list of one element id
    request = nx.search(param,limit=100, offset=0, search_type="usda")
    result = request.json()
    if result["total_hits"] >0:
        for item in result["hits"]: #is result hits top 10
            #item["fields"]["brand_name"]=="USDA" and  <- some ingredients dont have usda at least if worded differently
            print item["fields"]
            if (item["fields"]["nf_serving_size_unit"] == measurement or item["fields"]["nf_serving_size_unit"] == measurement+"s" or compare(item, measurement)):
                lists.append(item["fields"]["item_id"])
                lists.append(measurement)
                lists.append(amountfind(item,measurement))
                print "DONE"
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

    NF = ['nf_calories','nf_calories_from_fat','nf_total_fat','nf_saturated_fat','nf_trans_fatty_acid','nf_cholesterol','nf_sodium','nf_total_carbohydrate','nf_dietary_fiber','nf_sugars','nf_protein','nf_vitamin_a_dv','nf_vitamin_c_dv','nf_calcium_dv','nf_iron_dv']
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
        print x
        x.pop(0) #popping the amount 
        print x
        if check(x[0]):
            measurement = x[0]
            x.pop(0)
            searchL = clean(x)
        else:
            measurement="serving"
            searchL = clean(x)
    #search using the search params
        results = search(searchL, f2famount, measurement)
        print results
        resultid = results[0] #Nutritionix id of the search element
        print resultid
        measurement = results[1] #measurement used by the id which has been checked with measurement used in the passed recipe
        amount = results[2] #amount from Nutritionix database
        scalefactor = 1.0*amount/f2famount 
    #get nutri/allergen facts
        stats = getAstats(resultid)  #list of nutri facts, allergens
        #combine
        #print stats[0]
        nutri = scale(stats[0], scalefactor, nutri)
        allergens = list(set(stats[1]+allergens)) #double-check this to see if it removes duplicates
    return [nutri, allergens, measurement]
    #return searchL #we dont need to return the search Lists

############################FLASK COMMANDS################################
# this should go into the search engine part..... im using another html file just just test this out

##############NOT COMPLETED --- just a template to be completed later###########
@app.route("/nutrition", methods = ["GET"])
def run():
    source = ["3 skinless, boneless chicken breasts", "1 cup Italian seasoned bread crumbs", "1/2 cup grated Parmesan cheese", "1 teaspoon salt", "1 teaspoon dried thyme", "1 tablespoon dried basil", "1/2 cup butter, melted"]
    nutrifact = parser(source)
    n = nutrifact[0]
    allergen= nutrifact[1]
    measurement = nutrifact[2]
    #amount = nutrifact[3]
    
    return render_template("n.html",
                           #sizes = sizes,
                           #serverpcont = servercont,
                           #amountpserv = amountpserv,
                           calories = nformat(n,"nf_calories"),
                           fatcals = nformat(n,"nf_calories_from_fat"),
                           fat = nformat(n,"nf_total_fat"), 
                           fatdv = nformat(n,"nf_fat_dv"), 
                           satfat = nformat(n,"nf_saturated_fat"), 
                           satfatdv = nformat(n,"satfat_dv"),
                           transfat = nformat(n,"transfat"),
                           cholesterol = nformat(n,"nf_cholesterol"),
                           cholesteroldv = nformat(n,"cholesterol_dv"),
                           sodium = nformat(n,"nf_sodium"),
                           sodiumdv = nformat(n,"sodium_dv"),
                           carb = nformat(n,"nf_total_carbohydrate"), 
                           carbdv = nformat(n,"Carb-dv"),
                           df = nformat(n,"nf_dietary_fiber"), 
                           sugar = nformat(n,"nf_sugars"),
                           protein = nformat(n,"nf_protein"),
                           proteindv = nformat(n,"protein_dv"),
                           vitA = nformat(n,"nf_vitamin_a_dv"),
                           vitC = nformat(n,"nf_vitamin_a_dv"),
                           calcium = nformat(n,"nf_calcium_dv"),
                           iron= nformat(n,"nf_iron_dv"),
                           allergens = allergen
                           )


def nformat(dic, s):
    if s in dic.keys():
        return math.floor(dic[s])
    return 0
##########################################################################

############Testing Section
#print parser(["2 cups of apple juice"])
#print parser (["1 cup of apple juice"])
if __name__ == "__main__":
    app.debug=True
    app.run()

#####Some test output just for reference sake ### 
'''
sample output:
 u'allergen_contains_eggs': None,
 u'allergen_contains_fish': None,
 u'allergen_contains_gluten': None,
 u'allergen_contains_milk': None,
 u'allergen_contains_peanuts': None,
 u'allergen_contains_shellfish': None,
 u'allergen_contains_tree_nuts': None,
 u'allergen_contains_wheat': None,
 u'allergen_contains_soybeans': None, 

 u'brand_id': u'513fbc1283aa2dc80c000055',
 u'item_description': u'',
 u'item_id': u'529e7dd2f9655f6d35001d85',
 u'item_name': u'Cheese',
u'leg_loc_id': 116,

 u'nf_serving_size_qty': 1,
 u'nf_serving_size_unit': u'serving',
 u'nf_servings_per_container': None,

u'nf_serving_weight_grams': None, 

u'nf_calories': 60,
    nf_calories_from_fat': 40,
u'nf_total_fat': 4.5,
     u'nf_saturated_fat': 3,
     u'nf_trans_fatty_acid': None,
u'nf_cholesterol': 15,
u'nf_sodium': 90,
u'nf_total_carbohydrate': 1,
     u'nf_dietary_fiber': 0,
     u'nf_sugars': 0,
u'nf_protein': 4,

u'nf_vitamin_a_dv': 4,
 u'nf_vitamin_c_dv': 0,
  u'nf_calcium_dv': 10,
 u'nf_iron_dv': 0,


u'nf_monounsaturated_fat': None,
u'nf_polyunsaturated_fat': None,
 
u'nf_refuse_pct': None,

 
 u'nf_water_grams': None,
 u'old_api_id': None,
 u'updated_at': u'2012-04-18T04:05:59.000Z',
 u'usda_fields': None,
 u'brand_name': u'Desert Moon Grille', 
u'
{u'nf_ingredient_statement': None, 
'''

'''
dictionary fields of the api:
{   _score, _type, _id, fields{
          item_id,
          item_name,
          nf_serving_size_unit
            brand_name,
            nf_serving_size_qty,
          }
    _index
'''
