from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, viewsets
from rest_framework.decorators import action
from . serializers import ProductSerializer, CategorySerializer, FavoritSerializer, CategoryTypeSerializer
from . models import Product, Category, Favorit, ProductVariant, CategoryType



class CategoryTypeList(generics.ListAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FavoritView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoritSerializer
    queryset = Favorit.objects.all()

    @action(detail=False, methods=['get'], url_path='sync')
    def sync_favorit(self, request):
        user = request.user
        items = Favorit.objects.filter(user=user)

        serializer = FavoritSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='save')
    def save_basket_items(self, request):
        user = request.user


        items = request.data.get('items', [])
        for item in items:
            product_variant = get_object_or_404(ProductVariant, id=item['id'])
            favorit = Favorit.objects.create(product=product_variant, user=user)
            serializer = self.get_serializer(favorit)

        return Response({"message": "favorit items save successfully"},  status=status.HTTP_200_OK)










