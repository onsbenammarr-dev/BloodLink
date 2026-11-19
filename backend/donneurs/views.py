from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterDonneurSerializer


class RegisterDonneurView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = RegisterDonneurSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save()
        return Response({"detail": "Compte créé. Vous pouvez vous connecter."}, status=201)