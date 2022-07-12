from django.contrib import admin

from authentication.models import ForgotPassword


@admin.register(ForgotPassword)
class ForgotPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'done', 'created_at')
    list_filter = ('done', )
