from django.contrib import admin

# Register your models here.
from accounts.forms import UserProfileUpdateForm
from accounts.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # model = CustomUser
    form = UserProfileUpdateForm
    list_display = (
        "username",
        "first_name",
        "last_name",
        "nationality",
        "place_of_residence",
        "dob",
        "phone",
        "password",
    )
    # readonly_fields = ["password", "last_login"]
    list_filter = ("nationality", )

    custom_list_display = (
        "first_name",
        "last_name",
        "nationality",
        "place_of_residence",
        "dob",
        "phone",
        "email",
        "password",
    )
    search_fields = ['first_name', 'last_name', 'username']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


admin.site.register(CustomUser, CustomUserAdmin)
