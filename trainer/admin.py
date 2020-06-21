from django.contrib import admin
from .models import TrainerProfile, Certification, Experience, Workout, Exercise, Set, ExerciseImage
from client.models import ClientProfile


# Register your models here.

class ClientInline(admin.StackedInline):
    model = ClientProfile
    extra = 0


class CertificationInline(admin.StackedInline):
    model = Certification
    extra = 0


class ExperienceInline(admin.StackedInline):
    model = Experience
    extra = 0


class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    fieldsets = [
        ('Basic Info', {
            'fields': ['image', 'user', 'group', ('city', 'state')]
        }),
        ('Bio', {
            'fields': ['bio']
        })
    ]
    inlines = [CertificationInline, ExperienceInline, ClientInline]


admin.site.register(TrainerProfile, TrainerProfileAdmin)
admin.site.register(Certification)
admin.site.register(Experience)
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)
admin.site.register(ExerciseImage)