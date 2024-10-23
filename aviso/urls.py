from django.urls import path
from .views import check_url_view, agregar_servidor,register,eliminar_servidor,pausar_servidor, reanudar_servidor
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
     path('register/', register, name='register'),
    path('check_url/', check_url_view, name='check_url'),
    path('agregar_servidor/', agregar_servidor, name='agregar_servidor'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('eliminar_servidor/<str:server_name>/', eliminar_servidor, name='eliminar_servidor'),
    path('pausar_servidor/<str:server_name>/', pausar_servidor, name='pausar_servidor'),
    path('reanudar_servidor/<str:server_name>/', reanudar_servidor, name='reanudar_servidor')
]

router = routers.DefaultRouter()

