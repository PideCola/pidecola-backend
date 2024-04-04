from django.contrib import admin
from users.models import User, Vehicle, HonorificTitle
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Vehicle, admin.ModelAdmin)

@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = ('id', 'username','first_name','last_name', 'email', 'last_login', 'date_joined','is_active', 'is_staff','is_superuser', 'role')

    list_filter = ('is_active','first_name','last_name', 'is_superuser','is_staff')

    readonly_fields = ['last_login','date_joined','created_at', 'updated_at', 'rating', 'rating_count']

    search_fields = ('id', 'username', 'email')

    ordering = ('id', "username", "last_login")

    fieldsets = (
        ('User', {'fields': ('username',"first_name","last_name", 'email', 'password', 'role', 'groups', 'honorific_titles')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff')}),
        ('Dates', {'fields': ('created_at', 'updated_at', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )

    filter_horizontal = ('honorific_titles',)

class UserInline(admin.TabularInline):
    model = User.honorific_titles.through
    extra = 1

@admin.register(HonorificTitle)
class HonorificTitleAdmin(admin.ModelAdmin):
    inlines = [UserInline]