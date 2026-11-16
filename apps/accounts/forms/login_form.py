from django import forms


class LoginForm(forms.Form):
    """
    Form handling user authentication.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام کاربری',
            'autocomplete': 'username',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور',
            'autocomplete': 'current-password',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )
