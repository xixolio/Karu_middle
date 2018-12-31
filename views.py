# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cebolla.models import *
from rest_framework import generics
from django.contrib.auth.models import User
from cebolla.serializers import *
from rest_framework import permissions,viewsets



#class IngredientTypeList(generics.ListCreateAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
#    queryset = IngredientType.objects.all()
#    serializer_class = IngredientTypeSerializer

#class IngredientTypeDetail(generics.RetrieveUpdateDestroyAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = IngredientType.objects.all()
#    serializer_class = IngredientTypeSerializer

class IngredientTypeViewSet(viewsets.ModelViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer


#class PaymentTypeList(generics.ListCreateAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
#    queryset = PaymentType.objects.all()
#    serializer_class = PaymentTypeSerializer

#class PaymentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = PaymentType.objects.all()
#    serializer_class = PaymentTypeSerializer

class PaymentTypeViewSet(viewsets.ModelViewSet):
    queryset = PaymentType.objects.all()
    serializer_class = PaymentTypeSerializer

#class IngredientList(generics.ListCreateAPIView):
#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = Ingredient.objects.all()
#    serializer_class = IngredientSerializer
#    def perform_create(self, serializer):
#	ingredientType = IngredientType.objects.get(id=self.request.data['ingredientTypeId'])
#        paymentType = PaymentType.objects.get(id=self.request.data['paymentTypeId'])
#	serializer.save(ingredientType=ingredientType,paymentType=paymentType)

#class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Ingredient.objects.all()
#    serializer_class = IngredientSerializer

class IngredientViewSet(viewsets.ModelViewSet):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer
	def perform_create(self, serializer):
		ingredientType = IngredientType.objects.get(id=self.request.data['ingredientTypeId'])
	        paymentType = PaymentType.objects.get(id=self.request.data['paymentTypeId'])
		serializer.save(ingredientType=ingredientType,paymentType=paymentType)
	

#class LocalList(generics.ListCreateAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly)
#    queryset = Local.objects.all()
#    serializer_class = LocalSerializer

#class LocalDetail(generics.RetrieveUpdateDestroyAPIView):
#    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = Local.objects.all()
#    serializer_class = LocalSerializer

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

#class IngredientLocalList(generics.ListCreateAPIView):
#   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#    queryset = IngredientLocal.objects.all()
#    serializer_class = IngredientLocalSerializer
#    def perform_create(self, serializer):
#	ingredient = Ingredient.objects.get(id=self.request.data['ingredientId'])
#        local = Local.objects.get(id=self.request.data['localId'])
#	serializer.save(ingredient=ingredient,local=local)

#class IngredientLocalDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = IngredientLocal.objects.all()
#    serializer_class = IngredientLocalSerializer

class IngredientLocalViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = IngredientLocal.objects.all()
    serializer_class = IngredientLocalSerializer
    def perform_create(self, serializer):
	ingredient = Ingredient.objects.get(id=self.request.data['ingredientId'])
        local = Local.objects.get(id=self.request.data['localId'])
	serializer.save(ingredient=ingredient,local=local)

    def get_queryset(self):
	localUser = self.request.user.localUser
	if localUser.job != 'G':
		return IngredientLocal.objects.filter(local=localUser.local)
	else:
		return IngredientLocal.objects.all()

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    def perform_create(self, serializer):
	ingredientLocal = IngredientLocal.objects.get(id=self.request.data['ingredientLocalId'])
	serializer.save(ingredientLocal=ingredientLocal)

class DischargeViewSet(viewsets.ModelViewSet):
    queryset = Discharge.objects.all()
    serializer_class = DischargeSerializer
    def perform_create(self,serializer):
	ingredientLocal = IngredientLocal.objects.get(id=self.request.data['ingredientLocalId'])
	serializer.save(ingredientLocal=ingredientLocal)	

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
#    def perform_create(self,serializer):
#	local = Local.objects.get(id=self.request.data['localId'])
#	serializer.save(local=local)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    def perform_create(self,serializer):
	purchase = Purchase.objects.get(id=self.request.data['purchaseId'])
	serializer.save(purchase=purchase)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer 
    def perform_create(self,serializer):
	order = Purchase.objects.get(id=self.request.data['orderId'])
	localIngredient = LocalIngredient.objects.get(id=self.request.data['localIngredientId'])
	serializer.save(order=order,localIngredient=localIngredient)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

















