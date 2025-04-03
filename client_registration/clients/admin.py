from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("client_name", "dob", "national_id")
    search_fields = ("client_name", "national_id")

# Alternatively, use:
# admin.site.register(Client)

