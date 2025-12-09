# sequia/accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer, MeSerializer, PasswordChangeSerializer
)


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register
    Crea un usuario (sin requerir autenticación).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/auth/me    -> perfil del usuario
    PATCH/PUT /api/auth/me -> actualizar first_name/last_name
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """
    POST /api/auth/password/change
    Cambia la contraseña del usuario autenticado.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Contraseña actualizada."}, status=status.HTTP_200_OK)
