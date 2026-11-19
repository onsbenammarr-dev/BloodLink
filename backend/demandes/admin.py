from django.contrib import admin
from .models import DemandeSang, DossierPredon, Don, RendezVous

admin.site.register(DemandeSang)
admin.site.register(RendezVous)
admin.site.register(Don)
admin.site.register(DossierPredon)