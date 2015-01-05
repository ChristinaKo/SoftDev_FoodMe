import urllib2
import json
from nutritionix import Nutritionix
###################KEY INFO HERE FOR API ACCESS##################################

#nx = Nutritionix (api_key = "",
#                  app_id = "")

################################################################################

def search(param):
    lists=[]
    request = nx.search("cheese")
    result = request.json()
    print result["total_hits"]
    print result["hits"]
    print " "
    for item in result["hits"]:
        print item["fields"]
        print "Item Name: "+ item["fields"]["item_name"]+"\n Brand: "+item["fields"]["brand_name"]
        lists.append(item["fields"]["item_id"])
    return lists

def getstats(lists):
    for item_id in lists:
        print nx.item(id=item_id).json()

def getnutritionfacts(item_id):
    print nx.item(id=item_id).json()

def brandsearch(brand):
    print brand
    request= nx.brand().search(query=brand)
    result = request.json()
    print result
    if len(result)>0:
        print "BRAND: FOUND"

print "\n\n\n\n\n"
getstats(search("egg salad"))

'''
sample output:
{u'nf_ingredient_statement': None, 
u'nf_serving_weight_grams': None, 
u'allergen_contains_soybeans': None, 
u'brand_name': u'Desert Moon Grille', 
u'nf_calories_from_fat': 40,
 u'nf_calcium_dv': 10,
 u'brand_id': u'513fbc1283aa2dc80c000055',
 u'allergen_contains_eggs': None,
 u'nf_iron_dv': 0,
 u'nf_cholesterol': 15,
 u'item_description': u'',
 u'usda_fields': None,
 u'nf_monounsaturated_fat': None,
 u'nf_dietary_fiber': 0,
 u'item_name': u'Cheese',
 u'allergen_contains_tree_nuts': None,
 u'allergen_contains_shellfish': None,
 u'nf_vitamin_c_dv': 0,
 u'nf_polyunsaturated_fat': None,
 u'allergen_contains_peanuts': None,
 u'nf_sugars': 0,
 u'nf_servings_per_container': None,
 u'nf_total_fat': 4.5,
 u'nf_total_carbohydrate': 1,
 u'leg_loc_id': 116,
 u'nf_saturated_fat': 3,
 u'allergen_contains_wheat': None,
 u'old_api_id': None,
 u'updated_at': u'2012-04-18T04:05:59.000Z',
 u'allergen_contains_gluten': None,
 u'nf_protein': 4,
 u'item_id': u'529e7dd2f9655f6d35001d85',
 u'nf_calories': 60,
 u'nf_water_grams': None,
 u'allergen_contains_fish': None,
 u'nf_trans_fatty_acid': None,
 u'nf_serving_size_qty': 1,
 u'allergen_contains_milk': None,
 u'nf_vitamin_a_dv': 4,
 u'nf_serving_size_unit': u'serving',
 u'nf_refuse_pct': None,
 u'nf_sodium': 90}
'''

