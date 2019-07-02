from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from cebolla import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'ingredient',views.IngredientViewSet)
router.register(r'order',views.OrderViewSet)
router.register(r'price',views.PriceViewSet)
router.register(r'kitchenItem',views.KitchenItemViewSet)
router.register(r'purchase',views.PurchaseViewSet)
router.register(r'messages',views.MessagesViewSet)
#router.register(r'item',views.ItemViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]

