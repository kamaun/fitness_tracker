from django.contrib import admin
from .models import ClientProfile, BodyComposition, CardiorespiratoryAssessment


# Register your models here.

class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'trainer']
    fieldsets = [
        ('Basic Info', {
            'fields': ['image', ('user', 'trainer')]
        }),
        ('Bio', {
            'fields': ['bio']
        })
    ]


admin.site.register(ClientProfile, ClientProfileAdmin)
admin.site.register(BodyComposition)
admin.site.register(CardiorespiratoryAssessment)

