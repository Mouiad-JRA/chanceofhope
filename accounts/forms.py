from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm

from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs["required"] = "required"

    phone = PhoneNumberField()
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "User Name"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
        error_messages={"required": "Please fill in the details."},
    )

    password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password "}
        ),
        error_messages={"required": "Please fill in the details."},
    )

    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password confirmation"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    description = forms.CharField(max_length=255,
                                  widget=forms.Textarea(
                                      attrs={"class": "form-control", "placeholder": "Description"}
                                  ),
                                  error_messages={"required": "Please fill in the details."},
                                  )

    error_css_class = "error"

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "nationality",
            "dob",
            "place_of_residence",
            "address",
            "description",
            "sex",
            "age",
            "password1",
            "password2",
            "phone",
        )
        widgets = {
            "nationality": forms.Select(
                attrs={
                    "class": "form-control customselect1 dropdown",
                    "data-settings": '{"cutOff":5}',
                },
            ),
            "place_of_residence": forms.Select(
                attrs={
                    "class": "form-control customselect1 dropdown",
                    "placeholder": "Place of residence",
                    "data-settings": '{"cutOff":5}',
                }
            ),
            "dob": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "datepicker",
                    "placeholder": "Date of Birth",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Postal Address",
                    "required": "true",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control text-area",
                    "placeholder": "Description",
                }
            )
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError("This email has already been taken.")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError("This username has already been taken.")

    def clean_password(self):

        password = self.cleaned_data["password1"]
        confirm_password = self.cleaned_data["password2"]

        if password != confirm_password:
            raise forms.ValidationError("password and confirm password does not match")


class UserProfileUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Enter username',
            }
        )
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Enter First Name',
            }
        )
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Last Name',
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'Email',
            }
        )
        self.fields['phone'].widget.attrs.update(
            {
                'placeholder': 'Phone Number',
            }
        )
        self.fields['age'].widget.attrs.update(
            {
                'placeholder': 'Age',
            }
        )
        self.fields['sex'].widget.attrs.update(
            {
                'placeholder': 'sex',
            }
        )
        self.fields['dob'].widget.attrs.update(
            {
                'placeholder': 'dob',
            }
        )
        self.fields['description'].widget.attrs.update(
            {
                'placeholder': 'description',
            }
        )
        self.fields['address'].widget.attrs.update(
            {
                'placeholder': 'address',
            }
        )
        self.fields['place_of_residence'].widget.attrs.update(
            {
                'placeholder': 'place of residence',
            }
        )
        self.fields['nationality'].widget.attrs.update(
            {
                'placeholder': 'nationality',
            }
        )

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "age", "sex", "dob", "description", "address",
                  "place_of_residence",
                  "nationality", "profile_picture",

                  "phone", ]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].label = _("Email")
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = CustomUser.objects.filter(email=email).first()

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist.")

            if not self.user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")

        return super(UserLoginForm, self).clean()

    def get_user(self):
        return self.user

    def save(self):
        return CustomUser.objects.get(email=self.cleaned_data["login"])


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
