from rest_framework import permissions
from django.conf import settings


class HasValidAPIKeY(permissions.BasePermission):
    # configuracion de permisos para verificar si es una apikey validad al momento de un request
    
    def has_permission(self, request,view):
        api_key = request.headers.get("API-Key")
        return api_key in getattr(settings, "VALID_API_KEY",[])