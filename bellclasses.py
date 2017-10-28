# Taco-bell classes.
class Ingredient(object):
	def __init__(self, name, price):
		self.name = name
		self.price = price

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price

class Modifier(object):
	def __init__(self, name, price, ingredients):
		self.name = name
		self.price = price
		self.ingredients = ingredients

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price
	def getIngredients(self):
		return self.ingredients

class Derived_Product(object):
	def __init__(self, name, price, removed_items, is_fresco, is_supreme, added_items, difference, is_grilled):
		self.name = name
		self.price = price
		self.removed_items = removed_items
		self.is_fresco = is_fresco
		self.is_supreme = is_supreme
		self.added_items = added_items
		self.difference = difference
		self.is_grilled = is_grilled

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price
	def getRemovedItems(self):
		return self.removed_items
	def getIsFresco(self):
		return self.is_fresco
	def getIsSupreme(self):
		return self.is_supreme
	def getAddedItems(self):
		return self.added_items
	def getDifference(self):
		return self.difference
	def getIsGrilled(self):
		return self.is_grilled

class Product(object):
	def __init__(self, name, price, ingredients, URL, food_type, modifiers, grilled, fresco, supreme):
		self.name = name
		self.price = price
		self.ingredients = ingredients
		self.URL = URL
		self.food_type = food_type
		self.modifiers = modifiers
		self.grilled = grilled
		self.fresco = fresco
		self.supreme = supreme

	def setIngredients(self, ingredients):
		self.ingredients = ingredients
	def setModifiers(self, modifiers):
		self.modifiers = modifiers
	def setGrilled(self, grilled):
		self.grilled = grilled
	def setFoodType(self, food_type):
		self.food_type = food_type
	def setFresco(self, fresco):
		self.fresco = fresco;
	def setSupreme(self, supreme):
		self.supreme = supreme;

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price
	def getURL(self):
		return self.URL
	def getIngredients(self):
		return self.ingredients
	def getFoodType(self):
		return self.food_type
	def getModifiers(self):
		return self.modifiers
	def getGrilled(self):
		return self.grilled
	def getFresco(self):
		return self.fresco
	def getSupreme(self):
		return self.supreme


class Substitution(object):
	def __init__(self, name, price):
		self.name = name
		self.price = price

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price

class Combo(object):
	def __init__(self, name, price, ingredients, URL):
		self.name = name
		self.price = price
		self.ingredients = ingredients
		self.URL = URL

	def getName(self):
		return self.name
	def getPrice(self):
		return self.price
	def getURL(self):
		return self.URL
	def getIngredients(self):
		return self.ingredients
