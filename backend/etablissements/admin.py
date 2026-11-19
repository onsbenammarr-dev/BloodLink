from django.contrib import admin, messages

from .emails import envoyer_decision
from .models import Etablissement


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ("nom", "ville", "user", "statut_validation")
    list_filter = ("statut_validation",)
    list_editable = ("statut_validation",)
    search_fields = ("nom", "user__email")
    actions = ["valider", "refuser"]

    def save_model(self, request, obj, form, change):
        ancien = None
        if change:
            ancien = (
                Etablissement.objects.filter(pk=obj.pk)
                .values_list("statut_validation", flat=True)
                .first()
            )
        super().save_model(request, obj, form, change)
        if change and ancien != obj.statut_validation and obj.statut_validation in ("valide", "refuse"):
            envoyer_decision(obj)
            self.message_user(request, f"E-mail envoyé à {obj.user.email}.", messages.SUCCESS)

    def _decider(self, request, queryset, statut):
        n = 0
        for etab in queryset.exclude(statut_validation=statut).select_related("user"):
            etab.statut_validation = statut
            etab.save(update_fields=["statut_validation"])
            envoyer_decision(etab)
            n += 1
        self.message_user(
            request, f"{n} établissement(s) mis à jour, e-mail envoyé.", messages.SUCCESS
        )

    @admin.action(description="Valider les établissements sélectionnés (envoie un e-mail)")
    def valider(self, request, queryset):
        self._decider(request, queryset, "valide")

    @admin.action(description="Refuser les établissements sélectionnés (envoie un e-mail)")
    def refuser(self, request, queryset):
        self._decider(request, queryset, "refuse")