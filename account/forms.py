from django import forms
from django_phonenumbers.form.fields import PhoneNumberField

from account.models import CustomUser


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.widget.attrs["required"] = "required"

    phone = PhoneNumberField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
        error_messages={
            "required": "Please fill in the details.",
            "invalid": "Enter a valid " "phone number " "along with " "country code",
        },
    )
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
    age = forms.IntegerField(
        widget=forms.IntegerField(
            attrs={"class": "form-control", "placeholder": "Your age"}
        ),
        error_messages={"required": "Please fill in the details."},
    )
    sex = forms.CharField(
        max_length=1,
        widget=forms.CharField(
            attrs={"class": "form-control", "placeholder": "Your gender"}
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

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        # phone = self.cleaned_data["phone"]
        # dob = self.cleaned_data["dob"]
        #
        # place_of_residence = self.cleaned_data["place_of_residence"]
        # address = self.cleaned_data["address"]
        #
        # description = self.cleaned_data["description"]
        # training = self.cleaned_data["training"]
        #
        #
        # references = self.cleaned_data["references"]
        # nationality = self.cleaned_data["nationality"]

        if commit:
            user.save()
        return user

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
