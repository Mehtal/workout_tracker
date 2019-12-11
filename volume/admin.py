from django.contrib import admin
from .models import Rep, Exercice, Musclegroup, Session
# Register your models here.


class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('name', 'primarymg', )


admin.site.register(Musclegroup)
# admin.site.register(Muscle)
admin.site.register(Exercice, ExerciceAdmin)
admin.site.register(Rep)
admin.site.register(Session)
