from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from tinymce import models as tinymce_models


class CustomUser(AbstractUser):
    # username = None
    SEX_TYPE_MALE = 'M'
    SEX_TYPE_FEMALE = 'F'
    SEX_TYPE_CHOICES = [
        (SEX_TYPE_MALE, 'Male'),
        (SEX_TYPE_FEMALE, 'Female'),
    ]
    phone = PhoneNumberField(blank=False, null=True)
    nationality = CountryField(blank=False, null=True)
    place_of_residence = CountryField(blank=False, null=True)
    dob = models.CharField(_("date of birth"), max_length=48, null=True, blank=True)
    address = models.CharField(
        _("Postal Address"), max_length=500, null=True, blank=True
    )
    description = tinymce_models.HTMLField(blank=True, null=True)
    approved = models.BooleanField(_("Is Approved"), default=False, blank=True)
    sex = models.CharField(_("Sex"), choices=SEX_TYPE_CHOICES, default='F', max_length=1)
    profile_picture = models.ImageField(upload_to='images', null=True)
    email = models.EmailField(_('Email'), unique=True, blank=False, null=True,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    age = models.PositiveIntegerField(_('age'), blank=False, null=True,
                                      error_messages={
                                          'Negative integer': "Please enter a Valid age",
                                      })

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('', kwargs={'pk': self.pk})


    

