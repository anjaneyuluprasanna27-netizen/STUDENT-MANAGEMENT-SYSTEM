from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'full_name', 'email', 'course', 'phone', 'created_at')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('course',)
