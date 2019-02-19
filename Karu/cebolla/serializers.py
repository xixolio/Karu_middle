from rest_framework import serializers
from cebolla.models import *
from django.contrib.auth.models import User


class IngredientSerializer(serializers.ModelSerializer):
		id = serializers.IntegerField(required = True)
		class Meta:
			model = Ingredient
			fields = ('id', 'name','price','scale')
			
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
	#itemPrice = serializers.IntegerField(read_only=True)
	class Meta:
		model = Item
		fields = ('id','ingredient','amount','itemPrice')
		
	# def create(self,validated_data):
		# ingredientLocalId = validated_data.pop('ingredientLocal')
		# itemPrice = IngredientLocal.objects.get(pk=ingredientLocalId).price
		# item = Item.objects.create(**validated_data, itemPrice=itemPrice)
		# return item


class OrderSerializer(serializers.ModelSerializer):
#	algo = serializers.IntegerField()
	items = ItemSerializer(many=True, required=True)
	orderPrice = serializers.IntegerField(read_only=True)
	class Meta:
		model = Order
		fields = ('id','orderPrice','rfID','items','ongoing','receiving')
		
	def validate_items(self, items):
		if len(items) == 0:
			raise serializers.ValidationError('se requiere al menos un item')
		return items
		
	def update(self,instance,validated_data):
		
		items = validated_data.pop('items')
		
		for item in items:
			if not item.get('id'):
				amount = item.get('amount')
				ingredient = item.get('ingredient')
				itemPrice = item.get('itemPrice')
				Item.objects.create(amount=amount,itemPrice=itemPrice,ingredient=ingredient,order=instance)
			else:
				oldItem = Item.objects.get(id = item.get('id'))
				oldItem.amount += item.get('amount')
				oldItem.save()
		return instance






