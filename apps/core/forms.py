from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserProfile

# Classi CSS Tailwind riutilizzabili
_INPUT_CSS = (
    'w-full px-4 py-2.5 rounded-lg border border-gray-300 '
    'focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-all'
)
_TEXTAREA_CSS = _INPUT_CSS + ' resize-y min-h-[80px]'


class LoginForm(AuthenticationForm):
    """Form di login con styling Tailwind."""
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': _INPUT_CSS, 'placeholder': 'Il tuo username'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT_CSS, 'placeholder': 'La tua password'}),
    )


class RegisterForm(UserCreationForm):
    """Form di registrazione con validazione custom."""
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = _INPUT_CSS
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = 'Almeno 8 caratteri, non troppo comune'
        self.fields['password2'].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Questo username è già in uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Questa email è già registrata.')
        return email


class ProfileForm(forms.ModelForm):
    """Form per modificare il profilo."""
    class Meta:
        model = UserProfile
        fields = ('bio',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs['class'] = _TEXTAREA_CSS
        self.fields['bio'].label = 'Breve Bio'
