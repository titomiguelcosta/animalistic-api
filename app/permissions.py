from rest_framework import permissions
import os


class HasAuthToken(permissions.BasePermission):
    """
    Custom permission to only allow request with a token
    """

    def has_object_permission(self, request, view, obj):
        token = os.getenv('TOKEN', False)

        # if not token was set, assume api is public
        if not token:
            return True

        if token in [request.query_params['token'], token == request.data['token']]:
            return True

        return False
