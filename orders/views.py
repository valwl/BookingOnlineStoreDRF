from django.shortcuts import get_object_or_404
from . models import Basket, Orders
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions


from . serializers import OrdersCreateSerializer, BasketSerializer, BasketItemSerializer
from . services import OrderService
from . PaymentSerice import PaymentService
from .models import Basket, BasketItem
from product.models import ProductVariant


class BasketViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer

    @action(detail=False, methods=['get'], url_path='sync')
    def sync_basket(self, request):
         user = request.user
         basket, created = Basket.objects.get_or_create(user=user)
         basket_items = BasketItem.objects.filter(basket=basket)
         if created:
             return Response({"items": []})
         serializer = BasketItemSerializer(basket_items, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear')
    def clear_basket(self, request):
         user = request.user
         basket = get_object_or_404(Basket, user=user)
         basket.items.clear()
         return Response({"message": "Basket clear successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='save')
    def save_basket_items(self, request):

        user = request.user
        basket, created = Basket.objects.get_or_create(user=user)

        items = request.data.get('items', [])

        if not items:
            return Response({"message": "no item provider"}, status=status.HTTP_400_BAD_REQUEST)
        for item in items:
            product_variant = get_object_or_404(ProductVariant, id=item['id'])
            basket_item, created = BasketItem.objects.get_or_create(
                    basket=basket,
                    product=product_variant,
                    quantity=item['quantity']
                )

            if not created:
                basket_item.quantity = item['quantity']
                basket_item.save()
        return Response({"message": "Basket update successfully"}, status=status.HTTP_200_OK)





# class SaveBasketItemsView(generics.CreateAPIView):
#     queryset = BasketItem.objects.all()
#     serializer_class = BasketItemSerializer


# class SaveBasketItemsView(generics.ListCreateAPIView):
#     queryset = BasketItem.objects.all()
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return ApartmentCreateSerializers
#         return ApartmentSerializer
#
#     def perform_create(self, serializer):
#         apartment = serializer.save(user=self.request.user)
#         response_serializer = ApartmentCreateSerializers(apartment)
#         return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        phone = serializer.validated_data.get('phone')
        address = serializer.validated_data.get('address')
        try:
            order = OrderService.create_order(user, phone, address)
            serializer.instance = order
            # return Response(OrdersCreateSerializer(order).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class StripeCheckOutSessionView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = get_object_or_404(Orders, pk=order_id, basket__user=request.user)
            session_id = PaymentService.create_checkout_session(order)
            return Response({'session_id': session_id}, status=status.HTTP_200_OK)
        except Orders.DoesNotExist:
            return Response({'detail:' 'Order not found'}, status=status.HTTP_404_NOT_FOUND)




#1.  а где же функционал get or create for baskets
#2. почему используем viewsets если у на только функционал create in orderViewSet



# class CheckOutView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#
#         basket, created = Basket.objects.get_or_create(user=user)
#
#         order = Orders.objects.create(
#             basket=basket,
#             user=user,
#             phone=request.data.get('phone'),
#             address=request.data.get('address'),
#             total_cost=request.data.get('total_cost'),
#             status='pending',
#             # number=generation_order_number()
#         )
#
#         return Response(OrdersCreateSerializer(order).data, status=status.HTTP_201_CREATED)