from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    MAX_LENGTH_NAME = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-control not-required"
                if field_name in ("first_name", "last_name")
                else "form-control"
            )

            field.widget.attrs["id"] = f"{field_name}"

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if len(username) < 2:
            raise forms.ValidationError("Username must be at least 2 characters long.")

        if username.isdigit():
            raise forms.ValidationError("Username cannot contain digits only.")

        if not username[0].islower():
            raise forms.ValidationError("Username must start with a lowercase letter.")

        return username

    first_name = forms.CharField(max_length=MAX_LENGTH_NAME)
    last_name = forms.CharField(max_length=MAX_LENGTH_NAME)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )
