from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from demandes.constants import GROUPES
from .models import ProfilDonneur

User = get_user_model()


class RegisterDonneurSerializer(serializers.Serializer):
    prenom = serializers.CharField(max_length=60)
    nom = serializers.CharField(max_length=60)
    telephone = serializers.RegexField(
        r"^[0-9+ ]{8,20}$", error_messages={"invalid": "Numéro de téléphone invalide."}
    )
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    groupe_sanguin = serializers.ChoiceField(choices=GROUPES)
    ville = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Cet e-mail est déjà utilisé.")
        return value

    @transaction.atomic
    def create(self, data):
        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            role="donneur",
            first_name=data["prenom"],
            last_name=data["nom"],
        )
        return ProfilDonneur.objects.create(
            user=user,
            groupe_sanguin=data["groupe_sanguin"],
            ville=data["ville"],
            telephone=data["telephone"],
        )