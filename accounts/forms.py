from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import UserProfile


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


class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar información básica del usuario"""
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-dark text-white border-secondary',
            'placeholder': 'you@example.com'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': _('Username'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'readonly': 'readonly'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': _('First Name')
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': _('Last Name')
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar el perfil extendido del usuario"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'postal_code', 'receive_notifications']
        labels = {
            'phone': _('Phone Number'),
            'address': _('Address'),
            'city': _('City'),
            'country': _('Country'),
            'postal_code': _('Postal Code'),
            'receive_notifications': _('Receive Email Notifications'),
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': '+57 300 123 4567'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': _('Full address'),
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Bogotá'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Colombia'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': '110111'
            }),
            'receive_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input bg-dark border-secondary'
            }),
        }
