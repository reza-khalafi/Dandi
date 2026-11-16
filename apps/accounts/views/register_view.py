from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from apps.accounts.forms.register_form import RegisterForm
from apps.accounts.services.auth_service import AuthService


class RegisterView(View):
    """
    Handles user registration.
    """
    template_name = 'accounts/register.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('articles:home')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('articles:home')

        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data.get('email', '')

            user = self.auth_service.register_user(
                username=username,
                password=password,
                email=email
            )
            login(request, user)
            messages.success(request, f'خوش آمدید، {user.username}! حساب کاربری شما با موفقیت ایجاد شد.')
            return redirect('articles:home')

        return render(request, self.template_name, {'form': form})
