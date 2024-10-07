from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    name = serializers.CharField()
    location = serializers.CharField()
    services = serializers.ListField(child=serializers.DictField())  

class StatusResponseSerializer(serializers.Serializer):
    status_general = serializers.CharField()
    data = ServerSerializer(many=True)

