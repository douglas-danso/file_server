from django.contrib import admin
from authentication.models import CustomUser
from fileapp.models import File

class CustomUserAdmin(admin.ModelAdmin):
    pass

# class FileAdmin(admin.ModelAdmin):
#     list_display = ( 'downloads','emails_sent')

admin.site.register(CustomUser)
# admin.site.register(File, FileAdmin)
