from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from .models import Etablissement

User = get_user_model()


class EtablissementSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Etablissement
        fields = ["id", "nom", "ville", "statut_validation", "email"]
        read_only_fields = ["statut_validation"]


class RegisterEtablissementSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8) #write_only=True signifie que le mot de passe ne sera pas retourné dans la réponse JSON.
    nom = serializers.CharField(max_length=150)
    ville = serializers.CharField(max_length=100)

    #vérifie si l'email existe déjà
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():#filter() permet de rechercher des utilisateurs et email__iexact permet de comparer leurs emails sans tenir compte des majuscules et des minuscules.
            raise serializers.ValidationError("Cet e-mail est déjà utilisé.")
        return value

    @transaction.atomic
    def create(self, data):
        user = User.objects.create_user(
            email=data["email"], password=data["password"], role="etablissement"
        )
        return Etablissement.objects.create(user=user, nom=data["nom"], ville=data["ville"])