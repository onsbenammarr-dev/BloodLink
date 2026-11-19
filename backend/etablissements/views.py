from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsEtablissement
from .serializers import EtablissementSerializer, RegisterEtablissementSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        s = RegisterEtablissementSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        etab = s.save()
        return Response(EtablissementSerializer(etab).data, status=201)


class MonEtablissementView(APIView):
    permission_classes = [IsEtablissement]

    def get(self, request):
        return Response(EtablissementSerializer(request.user.etablissement).data)

    def patch(self, request):
        s = EtablissementSerializer(request.user.etablissement, data=request.data, partial=True)
        s.is_valid(raise_exception=True)
        s.save()
        return Response(s.data)