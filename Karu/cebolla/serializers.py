from rest_framework import serializers
from cebolla.models import *
from django.contrib.auth.models import User
from django.utils import timezone
import pytz
from django.conf import settings

class PriceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Price
		fields = ('name','price')

class IngredientSerializer(serializers.ModelSerializer):
		id = serializers.IntegerField(required = True)
		class Meta:
			model = Ingredient
			fields = ('id', 'name','price','scale','label')
			
		def validate_scale(self, scale):
			if scale > 0:
				if Ingredient.objects.filter(scale = scale).exists():
					query = Ingredient.objects.filter(scale = scale)
					print(self)
					if len(query) > 1:
						raise serializers.ValidationError('Dos ingredientes asignados a la misma pesa.')
					elif query[0].id != self.initial_data['id']:
						raise serializers.ValidationError('Dos ingredientes asignados a la misma pesa.')
			return scale

class ItemSerializer(serializers.ModelSerializer):
	# gets object based on its primary key
	id = serializers.IntegerField(required = False)
	ingredient = serializers.SlugRelatedField(slug_field = 'name',queryset=Ingredient.objects.all())
	order = serializers.SlugRelatedField(slug_field = 'name',read_only=True)
	#itemPrice = serializers.IntegerField(read_only=True)
	class Meta:
		model = Item
		fields = ('id','ingredient','amount','itemPrice','order')
		
	# def create(self,validated_data):
		# ingredientLocalId = validated_data.pop('ingredientLocal')
		# itemPrice = IngredientLocal.objects.get(pk=ingredientLocalId).price
		# item = Item.objects.create(**validated_data, itemPrice=itemPrice)
		# return item


class OrderSerializer(serializers.ModelSerializer):
#	algo = serializers.IntegerField()
	items = ItemSerializer(many=True, required=True)
	orderPrice = serializers.IntegerField()
	name = serializers.TextField(required=False)
	class Meta:
		model = Order
		fields = ('id','orderPrice','rfID','items','ongoing','receiving','name')
		
	def validate_items(self, items):
		if len(items) == 0:
			raise serializers.ValidationError('se requiere al menos un item')
		return items
		
	def update(self,instance,validated_data):
		
		print("Hola")
		items = validated_data.pop('items')
		instance.name = validated_data.pop('name')
		instance.orderPrice = validated_data.pop('orderPrice')
		previous_items = list(Item.objects.filter(order = instance))
		#print(previous_items)
		kitchen_labels = ['bases']
		for item in items:
			if not item.get('id'):
				amount = item.get('amount')
				ingredient = item.get('ingredient')
				itemPrice = item.get('itemPrice')
				item = Item.objects.create(amount=amount,itemPrice=itemPrice,ingredient=ingredient,order=instance)
				if item.ingredient.label in kitchen_labels:
					KitchenItem.objects.create(item = item, status = 'pedido', amount = amount)
			else:
				oldItem = Item.objects.get(id = item.get('id'))
				previous_items.remove(oldItem)
				oldItem = Item.objects.get(id = item.get('id'))
				amount = item.get('amount')
				increase = amount - oldItem.amount
				if oldItem.ingredient.label in kitchen_labels and increase > 0:
					if KitchenItem.objects.filter(item = oldItem).exclude(status = 'terminado').exists():
						kitchenItem = KitchenItem.objects.filter(item = oldItem).exclude(status = 'terminado')[0]
						#print(kitchenItem)
						#if kitchenItem.status != 'terminado':
						kitchenItem.status = 'actualizado'
						kitchenItem.amount += increase
						#else:
						#	kitchenItem = KitchenItem.objects.create(item = oldItem, status = 'pedido')
						#	kitchenItem.amount = increase
					else:
						kitchenItem = KitchenItem.objects.create(item = oldItem, status = 'pedido')
						kitchenItem.amount = increase
					kitchenItem.save()
				oldItem.amount = item.get('amount')
				oldItem.save()	
		for item in previous_items:
			item.delete()
		instance.save()
		return instance
		
class KitchenItemSerializer(serializers.ModelSerializer):
	# gets object based on its primary key
	item = ItemSerializer(required=True)

	#itemPrice = serializers.IntegerField(read_only=True)
	class Meta:
		model = KitchenItem
		fields = ('id','item','status','amount')
		
	def update(self,instance,validated_data):
		#item = validated_data.pop('item')
		instance.status = validated_data.pop('status')
		instance.save()
		return instance	
		
	# def create(self,validated_data):
		# ingredientLocalId = validated_data.pop('ingredientLocal')
		# itemPrice = IngredientLocal.objects.get(pk=ingredientLocalId).price
		# item = Item.objects.create(**validated_data, itemPrice=itemPrice)
		# return item

class DateTimeFieldWihTZ(serializers.DateTimeField):
	'''Class to make output of a DateTime Field timezone aware'''
	def to_representation(self, instance):
		format = "%Y-%m-%d %H:%M:%S"
		local_timezone = pytz.timezone(getattr(settings, 'America/New_York', None))
		representation = instance.astimezone(local_timezone).strftime(format)
		return representation
		
class MessagesSerializer(serializers.ModelSerializer):
	date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",default_timezone=pytz.timezone("Chile/Continental"),read_only=True)
	#date = DateTimeFieldWihTZ(read_only=True)
	class Meta:
		model = Messages
		fields = ('id','name','message','date')




