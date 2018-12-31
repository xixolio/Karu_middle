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
	

		

    
class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer 
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	




















