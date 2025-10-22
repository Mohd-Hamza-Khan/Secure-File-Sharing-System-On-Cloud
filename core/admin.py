from django.contrib import admin
from .models import SecureFile

@admin.register(SecureFile)
class SecureFileAdmin(admin.ModelAdmin):
    list_display = ("filename", "uploaded_by", "uploaded_at")
