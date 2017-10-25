from django.contrib import admin
from .models import *
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
        readonly_fields = ('project_week_number', 'project_actual_pgm')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Network)
admin.site.register(ProjectType)
admin.site.register(ProjectStatus)
