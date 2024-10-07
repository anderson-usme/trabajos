from .models import Project
from rest_framework import viewsets,permissions
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):#aqui decimos que consultas se pueden hacer
    queryset = Project.objects.all()#con esto consultamso todos los datos de una tabla
    permissions_classes = [permissions.AllowAny]
    serializer_class = ProjectSerializer