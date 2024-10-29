from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'favorit', views.FavoritView, basename='favorit')



urlpatterns = [
    path('product/', views.ProductList.as_view(), name='product_list'),
    path('category_type/', views.CategoryTypeList.as_view(), name='category_type'),
    path('detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('category/', views.CategoryListView.as_view(), name='category_list'),
    path('', include(router.urls)),



]

# path('favorit/save/', views.FavoritSaveItemView.as_view(), name='favorit_save'),