from rest_framework.permissions import BasePermission


#vérifier le rôle
class IsEtablissement(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(
            u.is_authenticated and u.role == "etablissement" and hasattr(u, "etablissement")
        )

#vérifier le rôle + validation
class IsEtablissementValide(IsEtablissement):
    message = "Votre établissement n'a pas encore été validé par l'administrateur."

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and request.user.etablissement.statut_validation == "valide"
        )