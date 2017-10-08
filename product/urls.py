from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = DefaultRouter()
router.register('appuser', views.AppuserViewset)

urlpatterns = [


    url(r'', include(router.urls)),
    url(r'^products/', views.ProductsAPIView.as_view()),
    url(r'^barcodes/', views.BarcodeScanAPIView.as_view()),
    url(r'^ratings/', views.RatingAPIView.as_view()),
    url(r'randtest/', views.RandomDataAPIView.as_view()),
]