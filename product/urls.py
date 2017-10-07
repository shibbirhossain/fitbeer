from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

#router.register('appusers', views.CustomerProfileChangeAPIView, "profile")
#router.register('appuser/password', views.ChangeAppUserPasswordView)
router = DefaultRouter()
#router.register('profile', views.UserProfileViewSet)
router.register('appuser', views.AppuserViewset)

urlpatterns = [

    #url(r'^appusers/invoke/', views.InvokeCameraView.as_view()),
    #url(r'^appusers/(?P<user_id>\d+)/photos/$', views.GetPhotosView.as_view()),
    # url(r'^appusers/photo/like/', views.LikePhotoView.as_view()),
    # url(r'^appusers/photo/unlike/', views.UnlikePhotoView.as_view()),
    # url(r'^appusers/(?P<user_id>.*)/photo/(?P<photo_id>.*)/like/', views.PhotoLikesView.as_view()),
    # url(r'^appusers/photos/$', views.PostPhotoView.as_view()),
    # url(r'^appusers/photo/(?P<photo_id>.*)/like/', views.PhotoLikesView.as_view()),
    # url(r'^appusers/photos/(?P<photo_id>.*)/comments/(?P<comment_id>\d+)', views.DeletePhotoCommentView.as_view()),
    # url(r'^appusers/photos/(?P<photo_id>.*)/comments/', views.PhotoCommentsView.as_view()),
    # url(r'^appusers/(?P<user_id>.*)/photos/posted/', views.PostedPhotosByUsersView.as_view()),
    url(r'', include(router.urls)),
    url(r'^products/', views.ProductsAPIView.as_view()),
    url(r'^barcodes/', views.BarcodeScanAPIView.as_view()),
    url(r'^ratings/', views.RatingAPIView.as_view()),
    #url(r'^test/', views.UnlikePhotoView.as_view()),
]