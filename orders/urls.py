from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BasketViewSet, OrderViewSet, StripeCheckOutSessionView
from . PaymentSerice import StripeWebhookView


router = DefaultRouter()
router.register(f'baskets', BasketViewSet)
router.register(f'orders', OrderViewSet, basename='order')
# router.register(f'payments', StripeCheckOutSessionView, basename='payment')


urlpatterns = [
    path('', include(router.urls)),

    path('payment_create/', StripeCheckOutSessionView.as_view(), name='payment_create'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),

    # path('baskets/save/', BasketViewSet.save_basket_items, name='save_basket'),
]