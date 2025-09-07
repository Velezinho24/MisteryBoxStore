from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_("Enter a valid email address"),
        label=_("Email"),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": _("Username"),
            "password1": _("Password"),
            "password2": _("Confirm password"),
        }

    def __init__(self, *args, **kwargs):
        """Aplica clases Bootstrap a todos los campos."""
        super().__init__(*args, **kwargs)
        common = {"class": "form-control bg-black text-white border-secondary"}

        self.fields["username"].widget.attrs.update(
            {**common, "placeholder": _("Username"), "autocomplete": "username"}
        )
        self.fields["email"].widget.attrs.update(
            {**common, "placeholder": _("you@example.com"), "autocomplete": "email", "inputmode": "email"}
        )
        self.fields["password1"].widget.attrs.update(
            {**common, "placeholder": _("Password"), "autocomplete": "new-password"}
        )
        self.fields["password2"].widget.attrs.update(
            {**common, "placeholder": _("Confirm password"), "autocomplete": "new-password"}
        )

        # Mensajes de ayuda más cortos (opcional)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
