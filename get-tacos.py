# Scrapes data from taco bell product listing page.
# want javascript class product-tile standard
import bellclasses as Bell
import os
import time
from selenium import webdriver

# os.remove(tacos_file)

# Ingredient list could have been parsed, but I just entered them all manually
ingredient_list = ["Reduced Fat Sour Cream", "Guacamole", "Pico De Gallo", "Chipotle Sauce", "Cheese", "Nacho Cheese Sauce", \
"Tomatoes", "Onions", "Red Sauce", "Spicy Ranch", "Lettuce", "Beans", "Jalapenos", "Avocado Ranch Sauce", "Potatoes", \
"Seasoned Rice", "Black Beans", "Fire Roasted Salsa", "Romaine Lettuce", "Seasoned Rice", "Chicken", "Shredded Chicken", \
"Steak", "Mexican Pizza Sauce", "Red Strips", "Grilled", "3 Cheese Blend", "Creamy Jalapeno Sauce"]
ingredient_price_list = [0.4, 0.4, 0.25, 0.3, 0.4, 0.55, 0.3, 0, 0, 0.3, 0.3, 0.25, 0.3, 0.3, 0.5, 0.3, 0.3, 0.45, 0.3, 0.6, \
1.3, 1.3, 1.5, 0.3, 0.25, 0, 0.4, 0.3]

ingredient_dictionary = {}

for i in range(28):
	tmp_name = ingredient_list[i]
	tmp_price = ingredient_price_list[i]
	tmp_object = Bell.Ingredient(tmp_name, tmp_price)
	ingredient_dictionary[tmp_name] = tmp_object

# Another manual list
modifier_dictionary = {}
supreme_mod_list = [ingredient_dictionary['Reduced Fat Sour Cream'], ingredient_dictionary['Tomatoes']]
fresco_mod_list = [ingredient_dictionary['Pico De Gallo']]
modifier_dictionary['Supreme'] = Bell.Modifier('Supreme', 0.60, supreme_mod_list)
modifier_dictionary['Fresco'] = Bell.Modifier('Fresco', 0.0, fresco_mod_list)

# www.tacobell.com/food/tacos contains the full product listing.
dir_path = os.path.dirname(os.path.realpath(__file__))
tacos_file = dir_path+"tmp/tacos.html"
drivers_file = dir_path+"/geckodriver" # Driver necessary for selenium

if os.path.isfile(tacos_file):
	# Thanks to: http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php	
	browser = webdriver.Firefox();
	url = "https://www.tacobell.com/food/tacos"
	browser.get(url)

	print "Waiting 5 seconds for the page to load"
	time.sleep(5)

	page = browser.page_source

	# There are some non-valid ascii characters, ignore them.
	page_encoded = page.encode('ascii', 'ignore').decode('ascii')

	browser.stop_client()
	browser.close()
	f = open('tmp/tacos.html', 'w')
	f.write(page_encoded)
	f.close()


f = open('tmp/tacos.html', 'r')

line = f.readline()

product_dict = {}

while line:
	is_new_item = line.find('data-price')
	
	# Potential product found
	if is_new_item >= 0:
		quote_start = line.find('"', is_new_item+11)
		quote_end = line.find('"', quote_start+1)
		price_length = quote_end - quote_start

		price_value = line[quote_start+1:quote_end]

		# There's one special case which falsely parses correctly
		if price_length == 2:
			line = f.readline()
			continue

		# Find the URL
		line = f.readline()

		is_product = line.find('a href')
		if is_product < 0:
			line = f.readline()
			continue
		is_drink = line.find('/drinks-and-sweets/')
		if is_drink >= 0:
			line = f.readline()
			continue
		is_breakfast = line.find('/breakfast/')
		if is_breakfast >= 0:
			line = f.readline()
			continue
		is_combo = line.find('/combos/')
		if is_combo >= 0:
			# Will eventually have different combo code
			line = f.readline()
			continue

		quote_start = line.find('"', is_product)
		quote_end = line.find('"', quote_start+1)

		URL_Value = line[quote_start+1:quote_end]

		title_start = URL_Value.rfind('/')
		product_title = URL_Value[title_start+1:]

		is_vegetarian = line.find('vegetarian')

		veg_modifier=""

		if is_vegetarian >= 0:
			veg_modifier="+VEG"

		product_title = product_title+veg_modifier


		if product_dict.has_key(product_title):
			line = f.readline()
			continue

		product_dict[product_title] = Bell.Product(product_title, price_value, [], URL_Value, "", [], False, False, False)

	line = f.readline()

f.close()


url_list = []

if False:
	browser = webdriver.Firefox();
	for key in product_dict:
		write_name = dir_path+"/tmp/"+product_dict[key].getName()
		print write_name

		if os.path.isfile(write_name):
			continue

		url_suffix = product_dict[key].getURL()
		url = "https://www.tacobell.com" + url_suffix

		browser.get(url)


		print "Waiting 7 seconds for the page to load"
		time.sleep(7)

		page = browser.page_source

		# There are some non-valid ascii characters, ignore them.
		page_encoded = page.encode('ascii', 'ignore').decode('ascii')

		f = open(write_name, 'w')
		f.write(page_encoded)
		f.close()


	browser.stop_client()
	browser.close()

food_type_list = ["doritos-cheesy-gordita-crunch-nacho-cheese", "crunchwrap-supreme", "quesarito", \
"nacho-cheese-doritos-locos-tacos-supreme", "nacho-cheese-doritos-locos-tacos", "fiery-doritos-locos-tacos-supreme", \
"fiery-doritos-locos-tacos", "cool-ranch-doritos-locos-tacos-supreme", "cool-ranch-doritos-locos-tacos", "crunchy-taco", \
"crunchy-taco-supreme", "soft-taco", "soft-taco-supreme", "chicken-soft-taco", "grilled-steak-soft-taco", \
"double-decker-taco", "double-decker-taco-supreme", "cheesy-gordita-crunch", "bean-burrito", "burrito-supreme", \
"7-layer-burrito", "beefy-5-layer-burrito", "xxl-grilled-stuft-burrito", "smothered-burrito", "shredded-chicken-burrito", \
"power-menu-burrito", "power-menu-burrito-veggie", "cheesy-potato-burrito", "combo-burrito", "black-bean-burrito", \
"cheesy-bean-and-rice-burrito", "beefy-nacho-griller", "chipotle-chicken-loaded-griller", "cheesy-potato-griller", \
"crispy-chicken-quesadilla", "naked-chicken-chips-6-pack", "steak-doubledilla", "chicken-doubledilla", \
"chicken-quesadilla", "cheese-quesadilla", "nachos-supreme", "nachos-bellgrande", "meximelt", "mexican-pizza", \
"gordita-supreme", "chalupa-supreme", "power-menu-bowl", "power-menu-bowl-veggie", "fiesta-taco-salad", "cheesy-roll-up", \
"chips-and-nacho-cheese-sauce", "chips-and-pico-de-gallo", "chips-and-guacamole", "chips-and-salsa", \
"cheesy-fiesta-potatoes", "pintos-n-cheese", "premium-latin-rice", "black-beans-and-rice", "black-beans", "doritos-chips", \
"spicy-potato-soft-taco", "beefy-fritos-burrito", "beefy-mini-quesadilla", "shredded-chicken-mini-quesadilla", \
"triple-layer-nachos", "spicy-tostada", "cinnabon-delights-2-pack", "caramel-apple-empanada", "cinnamon-twists", \
"7-layer-burrito+VEG", "bean-burrito+VEG", "black-bean-burrito+VEG", "cheesy-bean-and-rice-burrito+VEG", \
"power-menu-burrito-veggie+VEG", "power-menu-bowl-veggie+VEG", "cheesy-roll-up+VEG", "cheese-quesadilla+VEG", \
"spicy-tostada+VEG", "black-beans-and-rice+VEG", "pintos-n-cheese+VEG", "bean-burrito+VEG", "black-bean-burrito+VEG", \
"cheesy-bean-and-rice-burrito+VEG", "power-menu-burrito-veggie+VEG", "power-menu-bowl-veggie+VEG", "cheesy-roll-up+VEG", \
"cheese-quesadilla+VEG", "spicy-tostada+VEG", "black-beans-and-rice+VEG", "pintos-n-cheese+VEG"]

food_type_value = \
["dorito gordita", "other", "burrito", "nacho cheese doritos", "nacho cheese doritos", "fiery doritos", "fiery doritos", \
"cool ranch doritos", "cool ranch doritos", "hard taco", "hard taco", "soft taco", "soft taco", "soft taco", "soft taco", \
"other", "other", "gordita", "burrito", "burrito", "burrito", "burrito", "burrito", "other", "burrito", "burrito", "burrito", \
"burrito", "burrito", "burrito", "burrito", "burrito", "burrito", "burrito", "quesedilla", "other", "other", "other", \
"quesedilla", "quesedilla", "nachos", "nachos", "other", "tostado", "gordita", "other", "other", "other", "other", "rollup", \
"other", "other", "other", "other", "other", "other", "other", "other", "other", "other", "soft taco", "burrito", "other", \
"other", "nachos", "tostado", "other", "other", "other", "burrito", "burrito", "burrito", "burrito", "burrito", "other", \
"other", "quesedilla", "tostado", "other", "other", "burrito", "burrito", "burrito", "burrito", "other", "other", \
"quesedilla", "tostado", "other", "other"]

is_grilled_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#type_dict = {}

burrito_list = []
soft_taco_list = []
#quesedilla_list = []
#soft_taco_list = []

for i in range(90):
	tmp_name = food_type_list[i]
	tmp_value = food_type_value[i]
	is_grilled = is_grilled_values[i]
	if tmp_value == "other":
		#Remove other entries
		product_dict.pop(tmp_name, 0)
	else:
		if tmp_value == "burrito":
			burrito_list.append(tmp_name)
		if tmp_value == "soft taco":
			soft_taco_list.append(tmp_name)

		product_dict[tmp_name].setFoodType(tmp_value)
		product_dict[tmp_name].setGrilled(is_grilled)

for burrito in burrito_list:
	product_file = "tmp/"+product_dict[burrito].getName()

	f = open(product_file, 'r')

	line = f.readline()

	included_ingredients = []
	is_fresco = -1
	is_supreme = -1
	product_dict[burrito].setFresco(False)
	product_dict[burrito].setSupreme(False)
	while line:
		is_ingredient = line.find('div class="included"')
		
		if is_fresco < 0:
			is_fresco = line.find('data-name="make-it-fresco"')

		if is_supreme < 0:
			is_supreme = line.find('data-name="make-it-fresco"')

		# Ingredient found
		if is_ingredient >= 0:
			line = f.readline()
			line = f.readline()
			ingredient_start = line.find('>')
			ingredient_end = line.find('<', ingredient_start+1)


			tmp_ingredient = line[ingredient_start+1:ingredient_end]
			included_ingredients.append(tmp_ingredient)
		line = f.readline()

	f.close()
	
	product_dict[burrito].setIngredients(included_ingredients)
	if is_fresco >= 0:
		product_dict[burrito].setFresco(True)
	if is_supreme >= 0:
		product_dict[burrito].setSupreme(True)

sorted_price_list = []
unsorted_price_list = []


for i in range(len(burrito_list)):
	unsorted_price_list.append(product_dict[burrito_list[i]].getPrice());

tmp_burrito_list = burrito_list

i=1
while i < len(burrito_list):
	j=i
	while j > 0 and unsorted_price_list[j-1] > unsorted_price_list[j]:
		tmp_price = unsorted_price_list[j]
		unsorted_price_list[j] = unsorted_price_list[j-1]
		unsorted_price_list[j-1] = tmp_price
		j = j - 1
	i = i + 1

for i in range(len(burrito_list)):
	match_cost = unsorted_price_list[i]
	for j in range(len(burrito_list)):
		burrito_cost = product_dict[burrito_list[j]].getPrice()
		if burrito_cost == match_cost:
			sorted_price_list.append(burrito_list[j])
			burrito_list.pop(j)
			break

# Oops bad naming
sorted_name_list = sorted_price_list
sorted_price_list = unsorted_price_list

min_price = sorted_price_list[0]
parent_burrito_name = ""
parent_idx = 0

for i in range(len(sorted_price_list)):
	if sorted_price_list[i] > min_price:
		parent_burrito_name = sorted_name_list[i]
		parent_idx = i
		break


derived_children = {}

for i in range(parent_idx, len(sorted_price_list)):
	parent_burrito_name = sorted_name_list[i]

	parent_object = product_dict[parent_burrito_name]
	parent_cost = parent_object.getPrice()
	parent_ingredients = parent_object.getIngredients()
	children_objects = sorted_name_list[:i]

	min_product_cost = 1000000.00
	for j in range(len(children_objects)):
		child_object = product_dict[children_objects[j]]
		child_ingredients = child_object.getIngredients()
		child_is_fresco = child_object.getFresco()
		child_is_supreme = child_object.getSupreme()

		should_keep = []
		for k in range(len(child_ingredients)):
			if child_ingredients[k] in parent_ingredients:
				should_keep.append(True)
			else:
				should_keep.append(False)

		add_fresco = False


		items_to_remove = []
		for k in range(len(child_ingredients)):
			if not should_keep[k]:
				items_to_remove.append(child_ingredients[k])


		if child_is_fresco:
			if "Pico De Gallo" in parent_ingredients:
				if not "Nacho Cheese Sauce" in parent_ingredients and \
				not "Guacamole" in parent_ingredients and \
				not "Chipotle Sauce" in parent_ingredients and \
				not "Reduced Fat Sour Cream" in parent_ingredients and \
				not "Tomatoes" in parent_ingredients and \
				not "Creamy Jalapeno Sauce" in parent_ingredients and \
				not "3 Cheese Blend" in parent_ingredients and \
				not "Avocado Ranch Sauce" in parent_ingredients:
					add_fresco = True

		add_supreme = False
		if not add_fresco:
			if child_is_supreme:
				if "Reduced Fat Sour Cream" in parent_ingredients and "Tomatoes" in parent_ingredients:
					if not "Reduced Fat Sour Cream" in child_ingredients and \
					not "Tomatoes" in child_ingredients:
						add_supreme = True


		child_cost = float(child_object.getPrice())

		if add_fresco:
			child_ingredients.append("Pico De Gallo")

		if add_supreme:
			child_cost = child_cost+.80
			child_ingredients.append("Reduced Fat Sour Cream")
			child_ingredients.append("Tomatoes")


		add_on_items = []
		for k in range(len(parent_ingredients)):
			tmp_ingredient = parent_ingredients[k]
			if not tmp_ingredient in child_ingredients:
				if tmp_ingredient == "Seasoned Beef":
					child_cost = float(child_cost) + 1000.00
					break

				ingredient_cost = ingredient_dictionary[tmp_ingredient].getPrice()
				child_cost = child_cost + ingredient_cost
				add_on_items.append(tmp_ingredient)

		if float(child_cost) >= float(parent_cost):
			continue

		if float(child_cost) >= min_product_cost:
			continue

		min_product_cost = float(child_cost)

		child_object_name = child_object.getName()

		add_grilled = False

		if product_dict[parent_object.getName()].getGrilled():
			if not product_dict[child_object.getName()].getGrilled():
				add_grilled = True

		derived_child = Bell.Derived_Product(child_object.getName(), child_cost, items_to_remove, add_fresco, \
			add_supreme, add_on_items, float(parent_cost)-float(child_cost), add_grilled);

		if parent_object.getName() in derived_children:
			derived_children.pop(parent_object.getName(), 0)

		derived_children[parent_object.getName()] = derived_child

for key in derived_children:
	orig_price = product_dict[derived_children[key].getName()].getPrice()
	print key+", ($"+str(product_dict[key].getPrice())+"), "+derived_children[key].getName()+", ($" + \
		str(derived_children[key].getPrice())+", orig $"+orig_price+") - difference: "+str(derived_children[key].getDifference())
	print "Add these things: ", derived_children[key].getAddedItems()
	print "Remove these things: ", derived_children[key].getRemovedItems()
	if derived_children[key].getIsFresco():
		print "Add Fresco"
	if derived_children[key].getIsSupreme():
		print "Add Supreme"
	if derived_children[key].getIsGrilled():
		print "Add Grilled"
	print "\n"

"Fin"
