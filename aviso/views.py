import requests
from django.contrib.auth.models import User
from django.core.mail import send_mail  # Importa la función para enviar correos
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import StatusResponseSerializer, ServerSerializer

lista = [{
    "status_general": "",
    "servers": []
}]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  # Solo username y password

    def create(self, validated_data):
        user = User()
        user.username = validated_data['username']
        user.set_password(validated_data['password'])  # Encriptar la contraseña
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_url(request):
    global lista  # Asegúrate de que lista sea accesible
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
            # Enviar correo cuando el estado general pase a apagado
            send_mail(
                'Alerta: Estado del servidor apagado',
                'El estado general ha cambiado a apagado.',
                'anderusme@gmail.com',  # Remitente
                ['anderusme@gmail.com'],  # Destinatario
                fail_silently=False,
            )

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
                    # Enviar correo cuando el estado general pase a "apagado"
                    send_mail(
                        'Alerta: Estado del servidor apagado',
                        'El estado general ha cambiado a apagado.',
                        'anderusme@gmail.com',  # Remitente
                        ['anderusme@gmail.com'],  # Destinatario
                        fail_silently=False,
                    )

            return Response({'message': 'Servidor añadido exitosamente.'}, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
