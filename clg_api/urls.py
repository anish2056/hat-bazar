from django.urls import path

from clg_api.views.views_product_buy_create import ProductBuyCreateView
from .import views
urlpatterns = [
    path("login", views.LoginView.as_view(), name='login'),
    path("forgot/password", views.ForgorPasswordView.as_view(),name='forgot-password'),
    path("product/list", views.ProductListView.as_view(), name='product-list'),
    path("productSearch/list",views.ProductSearchListView.as_view(), name='product-search-list'),
    # vendor side
    path("vendor/register", views.VendorRegister.as_view(), name='vendor-signup'),
    path("product/create", views.ProductCreateView.as_view(), name='product-create'),
    path("province/list", views.ProvinceListView.as_view(), name='province-list'),
    path("district/list", views.DistrictListView.as_view(), name='district-list'),
    path("municipality/list", views.MunicipalityListView.as_view(), name='municipality-list'),
    path("vendor/product/list", views.VendorProductListView.as_view(), name='vendor-product-list'),
    # user side
    path("user/register", views.UserRegister.as_view(), name='vendor-signup'),
    path("vendor/signup", views.VendorSignupView.as_view(),name='vendor-signup'),
    path("category/list", views.CategoryListView.as_view(),name='category-list'),
    path("user/category/list", views.UserCategoryListView.as_view(),name='user-category-list'),
    path("sub/product/list", views.SubProductListView.as_view(),name='sub-product-list'),

    path("order/create", views.OrderCreateView.as_view(), name='order-create'),
    path("otp/generate", views.OtpGenerateListView.as_view(), name='otp-generate'),
    path("product/<pk>/buy", ProductBuyCreateView.as_view(), name='product-buy'),
    path('product/<pk>/findById',views.ProductFindByIdListView.as_view(), name='product-findbyid'),
    path('product/search/list',views.ProductSearchListView.as_view(), name='product-search-list'),
    path('product/prize/search/list', views.ProductPrizeListView.as_view(),name='product-search-list'),

    path('product/<pk>/comment',views.ProductCommentView.as_view(), name='product-comment-list'),
    path('product/<pk>/rating', views.ProductRatingView.as_view(),name='product-rating-list'),
    path('product/order/change/address', views.ProductOrderAddressChangeListView.as_view(),name='product-order-list'),
    path('addTo/card',views.AddToCardView.as_view(), name='add to card'),
    path('addTo/card/list', views.AddToCardListView.as_view(), name='add-to-card'),
    path('addTo/card/delete', views.AddToCardDeleteView.as_view(), name='add-to-card_delete'),
    path('product/bar/chart', views.ProducMatplotView.as_view(), name='add-to-card')

]
