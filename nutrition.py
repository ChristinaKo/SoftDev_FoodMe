import urllib2
import json
from nutritionix import Nutritionix

###################KEY INFO HERE FOR API ACCESS##################################
#you need to place an API key for Nutritionix here - provide one here below
nx = Nutritionix (api_key = "1f5463bda2c8668651d40bbb8b5ea1bf",
                  app_id = "1634d1d7")

################################################################################
#compares the item-name to find measurement words
def compare(item, measureu):
    temp = item["fields"]["item_name"].split()
    if measureu in temp:
        return True
    return False

#returns amount from Nutritionix database
def amountfind (item, measureu):
    temp = item["fields"]["item_name"].split()
    if measureu in temp:
        try:
            print "from USDA NAME"
            return float(temp[temp.index(measureu)-1])
        except:
            print "ARRAY ERROR"
    print "from nutritionix database"
    return float(item["fields"]["serving_size_qty"])
        
##Scales nutrition facts and combines with the passed original info
def scale (dic, factor, orig):
    ans ={}
    x = dic.keys()
    for key in x:
        try:
            ans[key] = dic[key]*factor
        except:
            pass
    #None 
        if len(orig) > 0: #if something in orig
            try:
                ans[key] = orig[key] + ans[key]
            except:
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

###############################API CALL FUNCTION#######################################
#'''''''''''''''''''''''''''''''''''''''''SEARCHING''''''''''''''''''''''''''''''''''''''''''''''''''''#

#returns one result of a search of params (using amounts and measurements as qualifiers)
#checks measurement and amounts
def search(param, amount, measurement):
   # print param
    lists=[] # list of one element id
    request = nx.search(param,limit=100, offset=0,search_type="usda")
    result = request.json()
    if result["total_hits"] >0:
        for item in result["hits"]: #is result hits top 10
            if  item["fields"]["brand_name"]=="USDA" and (item["fields"]["nf_serving_size_unit"] == measurement or compare(item, measurement) ):
                lists.append(item["fields"]["item_id"])
                lists.append(measurement)
                lists.append(amountfind(item,measurement))
                return lists   # list of one element
            
#parses through list of item_ids and searches for nutrition facts     
def getAstats(item_id):
    allergen= ["allergen_contains_eggs","allergen_contains_fish","allergen_contains_gluten","allergen_contains_milk","allergen_contains_peanuts","allergen_contains_shellfish","allergen_contains_tree_nuts","allergen_contains_wheat", "allergen_contains_soybeans"]
    nutrifacts= nx.item(id=item_id).json()
    LT = [] #List of allergens
    for n in allergen:
        if nutrifacts[n] != None:
            LT.append(n[18:])
    NF = ['nf_calories','nf_calories_from_fat','nf_total_fat','nf_saturated_fat','nf_trans_fatty_acid','nf_cholesterol','nf_sodium','nf_total_carbohydrate','nf_dietary_fiber','nf_sugars','nf_protein','nf_vitamin_a_dv','nf_vitamin_c_dv','nf_calcium_dv','nf_iron_dv']
    fact = {}
    for f in NF:
        fact[f] = nutrifacts[f]
    return [fact, LT]



#''''''''''''''''''''''''''''''''''''''''''' Main Function  ''''''''''''''''''''''''''''''''''''#

    
################################Parses and then searches#########################
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
        f2famount=float(x[0])
        x.pop(0) #popping the amount 
        if check(x[0]):
            measurement=x[0]
            x.pop(0)
            searchL= clean(x)
        else:
            measurement=0
            searchL=clean(x)
            
    #amount, measurement, searchL
    #search using the search params
        print searchL, f2famount, measurement
        results = search(searchL, f2famount, measurement)
        resultid = results[0] #Nutritionix id of the search element
        measurement = results[1] #measurement used by the id which has been checked with measurement used in the passed recipe
        amount = results[2] #amount from Nutritionix database
        scalefactor = 1.0*amount/f2famount 
    #get nutri/allergen facts
        stats = getAstats(resultid)  #list of nutri facts, allergens
        #combine
        #print stats[0]
        nutri = scale(stats[0], scalefactor, nutri)
        allergens = list(set(stats[1]+allergens)) #double-check this to see if it removes duplicates
    print [nutri, allergens]
    return searchL




############Testing Section
test = [' 3 skinless, boneless chicken breasts', ' 1 cup Italian seasoned bread crumbs', ' 1/2 cup grated Parmesan cheese', ' 1 teaspoon salt', ' 1 teaspoon dried thyme', ' 1 tablespoon dried basil', ' 1/2 cup butter, melted'] 

#x = search("apple juice",1,"cup")
#getNstats(x)

print parser(["1 cup of apple juice"])

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
