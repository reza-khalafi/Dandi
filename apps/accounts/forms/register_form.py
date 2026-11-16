from django import forms
from django.core.exceptions import ValidationError
from apps.accounts.repositories.user_repository import UserRepository


class RegisterForm(forms.Form):
    """
    Form handling new user registration.
    """
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'نام کاربری (حداقل ۳ کاراکتر انگلیسی)',
            'autocomplete': 'username',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ایمیل (اختیاری)',
            'autocomplete': 'email',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )
    password = forms.CharField(
        min_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'رمز عبور (حداقل ۶ نویسه)',
            'autocomplete': 'new-password',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )
    password_confirm = forms.CharField(
        min_length=6,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'تکرار رمز عبور',
            'autocomplete': 'new-password',
            'class': 'w-full px-4 py-3 rounded-xl border border-border-color bg-card-bg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-purple/60 focus:border-brand-purple transition duration-200'
        })
    )

    def clean_username(self) -> str:
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 3:
            raise ValidationError('نام کاربری باید حداقل ۳ کاراکتر باشد.')
        if UserRepository.exists_by_username(username):
            raise ValidationError('این نام کاربری قبلاً انتخاب شده است.')
        return username

    def clean(self) -> dict:
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'رمزهای عبور وارد شده همخوانی ندارند.')

        return cleaned_data
