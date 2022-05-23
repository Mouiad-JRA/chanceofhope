from django.contrib import admin

# Register your models here.
from account.forms import UserProfileUpdateForm
from account.models import CustomUser


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
    )
    search_fields = ['first_name', 'last_name', 'username']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


admin.site.register(CustomUser, CustomUserAdmin)
