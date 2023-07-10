from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User


class UserRegistrationForm(auth_forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = (
                "form-control not-required"
                if field_name in ("first_name", "last_name")
                else "form-control"
            )

            field.widget.attrs["id"] = field_name

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "This email address is already in use.")

        if len(username) < 2:
            self.add_error("username", "Username must be at least 2 characters long.")

        if username.isdigit():
            self.add_error("username", "Username cannot contain digits only.")

        if not username[0].islower():
            self.add_error("username", "Username must start with a lowercase letter.")

        return cleaned_data

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

