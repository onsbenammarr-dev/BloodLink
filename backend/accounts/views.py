from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            request,
            username=request.data.get("email"),
            password=request.data.get("password"),
        )
        if not user:
            return Response({"detail": "E-mail ou mot de passe incorrect."}, status=400)

        if user.role == "etablissement":
            statut = getattr(getattr(user, "etablissement", None), "statut_validation", None)
            if statut != "valide":
                if statut == "refuse":
                    msg = "Votre inscription a été refusée par l'administrateur."
                else:
                    msg = "Votre compte est en attente de validation par l'administrateur."
                return Response({"detail": msg}, status=403)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "role": user.role, "email": user.email})


class ChangerMotDePasseView(APIView):
    def post(self, request):
        ancien = request.data.get("ancien") or ""
        nouveau = request.data.get("nouveau") or ""
        if not request.user.check_password(ancien):
            return Response({"detail": "Mot de passe actuel incorrect."}, status=400)
        try:
            validate_password(nouveau, request.user)
        except ValidationError as e:
            return Response({"detail": " ".join(e.messages)}, status=400)
        request.user.set_password(nouveau)
        request.user.save()
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        return Response({"token": token.key})