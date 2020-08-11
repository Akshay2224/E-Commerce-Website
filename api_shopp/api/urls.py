from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from . import views
app_name = 'api'


router = routers.DefaultRouter()
router.register(r'product', views.ProductViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'Account', views.AccountViewSet)

urlpatterns = [
    path("shop/", views.index, name="ShopHome"),
    path("shop/about/", views.about, name="AboutUs"),
    path("shop/contact/", views.contact, name="ContactUs"),
    path("shop/search/", views.search, name="Search"),
    path("shop/checkout/", views.checkout, name="Checkout"),
    path("shop/products/<int:myid>", views.productView, name="ProductView"),
    path("shop/tracker/", views.tracker, name="TrackingStatus"),
    url(r'^$', views.user_login, name='user_login'),
    url(r'^sellerregd/$', views.register_seller, name="seller_register"),
    url(r'^sellerlogin/$', views.seller_login, name="seller_login"),
    url(r'^register/$', views.user_register, name='user_register'),
    path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^thanks/$', views.thanks, name="thanks")
]
