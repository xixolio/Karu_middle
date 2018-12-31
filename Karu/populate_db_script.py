import cebolla.models
from cebolla.models import *
#import numpy as np



ingredients = ['cebolla','tomate','palta','pimenton']
prices = [10]*len(ingredients)


for ingredient,price in zip(ingredients, prices):
	
	if not Ingredient.objects.filter(name = ingredient).exists():
		Ingredient.objects.create(name = ingredient, price = price)

ingredient = Ingredient.objects.get(name = ingredients[0])
order = Order.objects.create(cardId = 1)
Item.objects.create(ingredient = ingredient, order = order, amount = 50, itemPrice = 10)

