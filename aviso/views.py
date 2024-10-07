import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import StatusResponseSerializer, ServerSerializer

# 
lista = [{
    "status_general": "",
    "servers": []
}]

# Bearer para la autenticacion
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']  # Solo username y password

    def create(self, validated_data):
        user = User()  # Crear objeto usuario vacío
        user.username = validated_data['username']  # Asignar el username
        user.password = validated_data['password']  # Asignar la contraseña

        user.set_password(user.password)  # Encriptar la contraseña
        user.save()  # Guardar usuario en la base de datos

        return user  # Devolver el usuario

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_url(request):
    # Aquí empezamos a verificar el estado de cada servicio
    for server in lista[0]['servers']:
        for service in server['services']:
            for server_type in ['backend', 'frontend']:
                url = service[server_type]['url']
                try:
                    response = requests.get(url)  # Hacemos la petición
                    if response.status_code == 200:
                        service[server_type]['status'] = "activo"  # Si está activo
                    else:
                        service[server_type]['status'] = "apagado"  # Si está apagado
                except:
                    service[server_type]['status'] = "Error"  # Si hay error

    # Comprobamos si todos los servicios están activos
    todos_activos = True
    for server in lista[0]['servers']:
        for service in server['services']:
            if service['backend']['status'] != "activo" or service['frontend']['status'] != "activo":
                todos_activos = False  # Si no todos están activos

    if todos_activos:
        lista[0]['status_general'] = "activo"
    else:
        lista[0]['status_general'] = "apagado"

    # Serializar la respuesta
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
            
            # Añadir el nuevo servidor a la lista
            lista[0]['servers'].append(new_server)

            # Comprobar el estado de los servicios añadidos
            for service in new_server['services']:
                for server_type in ['backend', 'frontend']:
                    url = service[server_type]['url']
                    try:
                        response = requests.get(url)  # Hacemos la petición
                        if response.status_code == 200:
                            service[server_type]['status'] = "activo"  # Si está activo
                        else:
                            service[server_type]['status'] = "apagado"  # Si está apagado
                    except:
                        service[server_type]['status'] = "Error"  # Si hay error

            # Comprobar si todos los servicios están activos
            todos_activos = True
            for service in new_server['services']:
                if service['backend']['status'] != "activo" or service['frontend']['status'] != "activo":
                    todos_activos = False  # Si no todos están activos

            if todos_activos:
                lista[0]['status_general'] = "activo"
            else:
                lista[0]['status_general'] = "apagado"

            return Response({'message': 'Servidor añadido exitosamente.'}, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

