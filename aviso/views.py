import requests
import threading
import time
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import StatusResponseSerializer, ServerSerializer

# Lista global para almacenar el estado de los servidores
lista = [{
    "status_general": "",
    "servers": []
}]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.save()
        return user

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def check_url():
    global lista
    while True:
        for server in lista[0]['servers']:
            for service in server['services']:
                for server_type in ['backend', 'frontend']:
                    url = service[server_type]['url']
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            service[server_type]['status'] = "activo"
                        else:
                            service[server_type]['status'] = "apagado"
                    except:
                        service[server_type]['status'] = "Error"

        todos_activos = True
        for server in lista[0]['servers']:
            for service in server['services']:
                if service['backend']['status'] != "activo" or service['frontend']['status'] != "activo":
                    todos_activos = False

        if todos_activos:
            nuevo_status = "activo"
        else:
            nuevo_status = "apagado"

        if nuevo_status != lista[0]['status_general']:
            lista[0]['status_general'] = nuevo_status
            
            if nuevo_status == "apagado":
                send_mail(
                    'Alerta: Estado del servidor apagado',
                    'El estado general ha cambiado a apagado.',
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
        
        # Pausa la ejecución del hilo durante 60 segundos
        time.sleep(60)

# Iniciar el hilo en la configuración del servidor
threading.Thread(target=check_url, daemon=True).start()  # el daemon hace que el programa principal no se cierre y si se cierra este también

@api_view(['GET'])
def check_url_view(request):
    """
    Esta función permite a los usuarios consultar el estado actual de 
    los servidores y servicios. Devuelve un resumen del estado general 
    y la información detallada de cada servidor. La información se actualiza automáticamente cada 60 segundos 
    gracias a la función check_url que se ejecuta en segundo plano.
    """
    data = {
        "status_general": lista[0]['status_general'],
        "data": lista[0]['servers']
    }
    serializer = StatusResponseSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_servidor(request):
    if request.method == 'POST':
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            new_server = serializer.validated_data
            lista[0]['servers'].append(new_server)

            for service in new_server['services']:
                for server_type in ['backend', 'frontend']:
                    url = service[server_type]['url']
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            service[server_type]['status'] = "activo"
                        else:
                            service[server_type]['status'] = "apagado"
                    except:
                        service[server_type]['status'] = "Error"

            todos_activos = True
            for service in new_server['services']:
                if service['backend']['status'] != "activo" or service['frontend']['status'] != "activo":
                    todos_activos = False

            if todos_activos:
                nuevo_status = "activo"
            else:
                nuevo_status = "apagado"

            if nuevo_status != lista[0]['status_general']:
                lista[0]['status_general'] = nuevo_status
                
                if nuevo_status == "apagado":
                    send_mail(
                        'Alerta: Estado del servidor apagado',
                        'El estado general ha cambiado a apagado.',
                        settings.EMAIL_HOST_USER,
                        [settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    )

            return Response({'message': 'Servidor añadido exitosamente.'}, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

