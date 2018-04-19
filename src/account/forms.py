from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _
from django.utils.text import capfirst

User = get_user_model()


class AccountLoginForm(forms.Form):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
        'access_denied': _("Votre compte n'est pas autorisé")
    }

    username = forms.CharField(
        required=True,

        label=_('Nom d\'utilisateur'), widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d\'utilisateur',
            'autofocus': True
        }))
    password = forms.CharField(label=_('Mot de passe'), required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Votre mot de passe'
    }))

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request

        self.user_cache = None
        super(AccountLoginForm, self).__init__(*args, **kwargs)
        # Set the label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        # if self.fields['username'].label is None:
        #     self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        else:
            if not user.is_staff:
                raise forms.ValidationError(
                    self.error_messages['access_denied'],
                    code='access_denied',
                )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
