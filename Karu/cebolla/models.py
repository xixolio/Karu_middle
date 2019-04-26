# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from django.contrib.auth.models import User


class Ingredient(models.Model):
	name = models.CharField(max_length=255) #Removed unique, since at this stage what matters is only price and scale
	price = models.IntegerField()
	scale = models.IntegerField(default = 0)
	label = models.TextField(default = '')
	@property
	def generic_name(self):
		 "returns a generic name for the object, made of the local location and ingredient name"
		 return '%s' % (self.ingredient.name)


class rfID(models.Model):
	hex_id = models.CharField(max_length=255, unique = True)
	
class Order(models.Model):

	orderPrice = models.IntegerField(default=0)
	#cardId = models.IntegerField()
	rfID = models.OneToOneField(rfID,related_name='order', on_delete=models.PROTECT, default=1)
	ongoing = models.BooleanField(default = False)
	receiving = models.PositiveIntegerField(default = 0)

class Item(models.Model):

	order = models.ForeignKey(Order,related_name='items', on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient,related_name='items', on_delete=models.PROTECT)
	amount = models.IntegerField()
	itemPrice = models.IntegerField()
	
	class Meta:
		unique_together = ["order", "ingredient"]
		
	# def save(self, *args, **kwargs):
		
		# #self.itemPrice = self.ingredient.price()
		# self.order.orderPrice += self.itemPrice
			
		# super(Item, self).save(*args, **kwargs)


			

	
	


	
	

# Create your models here.
