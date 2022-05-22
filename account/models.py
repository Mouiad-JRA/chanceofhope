from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from tinymce import models as tinymce_models


class CustomUser(AbstractUser):
    phone = PhoneNumberField(blank=False, null=True)
    nationality = CountryField(blank=False, null=True)
    place_of_residence = CountryField(blank=False, null=True)
    dob = models.CharField(_("date of birth"), max_length=48, null=True, blank=True)
    address = models.CharField(
        _("Postal Address"), max_length=500, null=True, blank=True
    )
    description = tinymce_models.HTMLField(blank=True, null=True)
    approved = models.BooleanField(_("Is Approved"), default=False, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email
