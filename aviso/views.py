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
                        service[server_type]['status'] = "activo" if response.status_code == 200 else "apagado"
                    except:
                        service[server_type]['status'] = "Error"

        todos_activos = all(service[server_type]['status'] == "activo" for server in lista[0]['servers'] for service in server['services'] for server_type in ['backend', 'frontend'])

        nuevo_status = "activo" if todos_activos else "apagado"
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
        
        time.sleep(60)

threading.Thread(target=check_url, daemon=True).start()

@api_view(['GET'])
def check_url_view(request):
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
                        service[server_type]['status'] = "activo" if response.status_code == 200 else "apagado"
                    except:
                        service[server_type]['status'] = "Error"

            todos_activos = all(service[server_type]['status'] == "activo" for service in new_server['services'] for server_type in ['backend', 'frontend'])
            nuevo_status = "activo" if todos_activos else "apagado"

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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_servidor(request, server_name):
    global lista
    
    server_to_delete = None

    # Busca el servidor por su nombre
    for server in lista[0]['servers']:
        if server.get('name') == server_name:
            server_to_delete = server
            break  

    if server_to_delete:
        lista[0]['servers'].remove(server_to_delete)
        return Response({'message': 'Servidor eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Servidor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

