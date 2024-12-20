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
server_list = [{
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
    global server_list
    while True:
        for server in server_list[0]['servers']:
            if server.get('status') == 'pausado':
                continue  # Ignora este servidor si está pausado

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

        all_active = all(
            service[server_type]['status'] == "activo" 
            for server in server_list[0]['servers'] 
            for service in server['services'] 
            for server_type in ['backend', 'frontend']
            if server.get('status') != 'pausado'
        )

        if all_active:
            new_status = "activo"
        else:
            new_status = "apagado"

        if new_status != server_list[0]['status_general']:
            server_list[0]['status_general'] = new_status
            
            if new_status == "apagado":
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
        "status_general": server_list[0]['status_general'],
        "data": server_list[0]['servers']
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
            new_server['paused'] = False  # Establecer el estado de pausa en False al agregar
            new_server['status'] = 'activo'  # Estado inicial del servidor
            server_list[0]['servers'].append(new_server)

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

            all_active = True
            for service in new_server['services']:
                if service['backend']['status'] != "activo" or service['frontend']['status'] != "activo":
                    all_active = False
            
            if all_active:
                new_status = "activo"
            else:
                new_status = "apagado"

            if new_status != server_list[0]['status_general']:
                server_list[0]['status_general'] = new_status

                if new_status == "apagado":
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
    global server_list
    
    server_to_delete = None

    # Busca el servidor por su nombre
    for server in server_list[0]['servers']:
        if server.get('name') == server_name:
            server_to_delete = server
            break  

    if server_to_delete:
        server_list[0]['servers'].remove(server_to_delete)
        return Response({'message': 'Servidor eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)
    
    return Response({'error': 'Servidor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pausar_servidor(request, server_name):
    global server_list

    # Busca el servidor por su nombre
    for server in server_list[0]['servers']:
        if server.get('name') == server_name:
            server['paused'] = True  # Establecer el estado de pausa en True
            server['status'] = 'pausado'  # Cambiar el estado a pausado
            # Cambia el estado de los servicios a 'pausado'
            for service in server['services']:
                for server_type in ['backend', 'frontend']:
                    service[server_type]['status'] = 'pausado'
            return Response({'message': 'Servidor pausado exitosamente.'}, status=status.HTTP_200_OK)

    return Response({'error': 'Servidor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reanudar_servidor(request, server_name):
    global server_list

    # Busca el servidor por su nombre
    for server in server_list[0]['servers']:
        if server.get('name') == server_name:
            server['paused'] = False  # Establecer el estado de pausa en False
            server['status'] = 'activo'  # Cambiar el estado a activo
            return Response({'message': 'Servidor reanudado exitosamente.'}, status=status.HTTP_200_OK)

    return Response({'error': 'Servidor no encontrado.'}, status=status.HTTP_404_NOT_FOUND)