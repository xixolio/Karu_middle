# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cebolla.models import *
from rest_framework import generics
#from django.contrib.auth.models import User
from cebolla.serializers import *
from rest_framework import permissions,viewsets




class IngredientViewSet(viewsets.ModelViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	
class PurchaseViewSet(viewsets.ModelViewSet):
	queryset = Purchase.objects.all()
	serializer_class = PurchaseSerializer
	def perform_create(self,serializer):
		#local = Local.objects.get(id=self.request.data['localId'])
		serializer.save()
    
		

    
class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer 
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PriceViewSet(viewsets.ModelViewSet):
	queryset = Price.objects.all()
	serializer_class = PriceSerializer
	
class KitchenItemViewSet(viewsets.ModelViewSet):
	queryset = KitchenItem.objects.all()
	serializer_class = KitchenItemSerializer 
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class MessagesViewSet(viewsets.ModelViewSet):
	queryset = Messages.objects.all()
	serializer_class = MessagesSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


















