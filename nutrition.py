import urllib2
import json
from nutritionix import Nutritionix

###################KEY INFO HERE FOR API ACCESS##################################
#you need to place an API key for Nutritionix here - provide one here below

################################################################################

###############################API CALL FUNCTIONS#########################################


#'''''''''''''''''''''''''''''''''''''''''SEARCHING''''''''''''''''''''''''''''''''''''''''''''''''''''#
#returns one result of a search of params (using amounts and measurements as qualifiers)
#checks measurement and amounts
def search(param, amount, measurement):
    lists=[] # list of one element id
    request = nx.search(param,limit=100, offset=0,search_type="usda")
    #request = nx.search(param)
    result = request.json()
    if result["total_hits"] >0:
        for item in result["hits"]: #is result hits top 10
            if  item["fields"]["brand_name"]=="USDA" and (item["fields"]["nf_serving_size_unit"] == measurement or compare(item["fields"]["item_name"], measurement)):
                lists.append(item["fields"]["item_id"])

                return lists   # list of one element
    return None

#compares the item-name to find measurement words
def compare(name, measureu):
    temp = name.split()
    if measureu in temp:
        return True
    return False

#returns amount from Nutritionix database
def amountfind (item, measureu):
    temp = item["fields"]["item_name"].split()
    if measureu in temp:
        try:
            print "from USDA NAME"
            print temp[temp.index(measureu)-1]
            return float(temp[temp.index(measureu)-1])
        except:
            break
    print "from nutritionix database"
    return float(item["fields"]["serving_size_qty"])
        
#parses through list of item_ids and looks for nutrition facts     
def getNstats(lists):
    for item_id in lists:
        allergen= ["allergen_contains_eggs","allergen_contains_fish","allergen_contains_gluten","allergen_contains_milk","allergen_contains_peanuts","allergen_contains_shellfish","allergen_contains_tree_nuts","allergen_contains_wheat", "allergen_contains_soybeans"]
        nutrifacts= nx.item(id=item_id).json()
        LT = [] #List of allergens
        for n in allergen:
            if nutrifacts[n] != "None":
                LT.append(n[18:])
            else:
                print "error"
        return LT
    return "error"
    #print nutrifacts

#given a brand name, will search ingredients of that brand
def brandsearch(brand):
    print brand
    request= nx.brand().search(query=brand)
    result = request.json()
    print result
    if len(result)>0:
        print "BRAND: FOUND"

#''''''''''''''''''''''''''''''''''''''''''' Nutrition Calculations ''''''''''''''''''''''''''''''''''''#
#parses through list of ingredients from food to fork and finds all nutrition facts
def parser(ingredlist):
    for i in ingredlist:
        searchL = "None"   
        amounts = 0
        measurement = []
        ingred = i.strip() 
    #start of parsing stuff
        x = ingred.split()
#ASSUMING that amount is the first element of this split list
        x.pop(0) #popping the amount 
        amounts.append(x[0])
        if check(x[0]):
            measurement.append(float(x[0]))
        else:
            measurement.append(0)
        searchL.append(parse(x)) 
    #amount, measurement, searchL
        #search using the search params
        results = search(searchL)       
        #record correct amount
        


#parses measurement words
def parse(splitlist):
    if check(splitlist[0]): #check to see if word after is a measurement word, if so, remove
        query = " ".join(splitlist[1:])
    else:
        query = " ".join(splitlist)
    return query
   
#checks to see no extraneous measurement words that will mess up search
def check(measurement):
    L = ["cup", "teaspoon", "tablespoon", "quart", "pint", "pound", "lb", "ounce",
        "cups", "teaspoons", "tablespoons", "quarts", "pints", "pounds", "lbs", "ounces", "oz"]
    return measurement in L


############Testing Section
test = [' 3 skinless, boneless chicken breasts', ' 1 cup Italian seasoned bread crumbs', ' 1/2 cup grated Parmesan cheese', ' 1 teaspoon salt', ' 1 teaspoon dried thyme', ' 1 tablespoon dried basil', ' 1/2 cup butter, melted'] 

#commas dont affect number of results, but NEED TO QUALITY CHECK SEARCH RESULTS WITH COMMA
#AMOUNTS/NUMBERS AFFECT RESULTS
x = search("apple juice",1,"cup")
getNstats(x)




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
