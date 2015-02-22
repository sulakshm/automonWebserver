from django.contrib import admin

from gps.models import GpsNode, GpsNodeMetrics

# Register your models here.

class MetricsInline(admin.TabularInline):
    model = GpsNodeMetrics
    extra = 1

class GpsNodeAdmin(admin.ModelAdmin):
    search_fields = ['ident']
    #list_filter = ['created']
    list_display = ('ident', 'user', 'created', 'was_active_recently')
    fieldsets = [
        (None, {'fields':['ident', 'user']}),
    ]
    inlines = [MetricsInline]

admin.site.register(GpsNode, GpsNodeAdmin)
