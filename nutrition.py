import urllib2
import json
from nutritionix import Nutritionix
###################KEY INFO HERE FOR API ACCESS##################################

################################################################################
def search(param):
    lists=[]
    request = nx.search(param)
    result = request.json()
    print result["total_hits"]
    if result["total_hits"] >0:
        print result["hits"]
        print " "
        counter = 0
        for item in result["hits"]:
            print "\n\nITEM:"
            print item
            print "\n"
            print item["fields"]
            counter += 1
            print counter
    #       print "Item Name: "+ item["fields"]["item_name"]+"\n Brand: "+item["fields"]["brand_name"]
            lists.append(item["fields"]["item_id"])
        return lists
    else:
        return None
    
def getstats(lists):
    print "item_id "
    for item_id in lists:
        print nx.item(id=item_id).json()
        getnutritionfacts(item_id)
        
def getnutritionfacts(item_id):
    allergen= ["allergen_contains_eggs","allergen_contains_fish","allergen_contains_gluten","allergen_contains_milk","allergen_contains_peanuts","allergen_contains_shellfish","allergen_contains_tree_nuts","allergen_contains_wheat", "allergen_contains_soybeans"]
    #print allergen
    nutrifacts= nx.item(id=item_id).json()
    LT = []
    for n in allergen:
        if nutrifacts[n] != "None":
            LT.append(n[18:])
        else:
            print "error"
    print nutrifacts
    print LT

def brandsearch(brand):
    print brand
    request= nx.brand().search(query=brand)
    result = request.json()
    print result
    if len(result)>0:
        print "BRAND: FOUND"

x= search("egg salad")
getstats(x)




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
 u'nf_calcium_dv': 10,

  u'nf_calories': 60,
 u'nf_cholesterol': 15,
 u'nf_dietary_fiber': 0,
 u'nf_iron_dv': 0,
 u'nf_monounsaturated_fat': None,
 u'nf_polyunsaturated_fat': None,
 u'nf_protein': 4,

 u'nf_refuse_pct': None,

 u'nf_saturated_fat': 3,

 u'nf_serving_size_qty': 1,
 u'nf_serving_size_unit': u'serving',
 u'nf_servings_per_container': None,

 u'nf_sodium': 90}
 u'nf_sugars': 0,
 u'nf_total_carbohydrate': 1,
 u'nf_total_fat': 4.5,
 u'nf_trans_fatty_acid': None,
 u'nf_vitamin_a_dv': 4,
 u'nf_vitamin_c_dv': 0,

 u'nf_water_grams': None,
 u'old_api_id': None,
 u'updated_at': u'2012-04-18T04:05:59.000Z',
 u'usda_fields': None,
 u'brand_name': u'Desert Moon Grille', 
u'nf_calories_from_fat': 40,
u'nf_serving_weight_grams': None, 
{u'nf_ingredient_statement': None, 
'''

