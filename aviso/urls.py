from django.urls import path
from .views import check_url_view, agregar_servidor,register
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
     path('register/', register, name='register'),
    path('check_url/', check_url_view, name='check_url'),
    path('agregar_servidor/', agregar_servidor, name='agregar_servidor'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

router = routers.DefaultRouter()

#urlpatterns = router.urls