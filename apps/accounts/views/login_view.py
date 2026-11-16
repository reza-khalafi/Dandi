from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from apps.accounts.forms.login_form import LoginForm
from apps.accounts.services.auth_service import AuthService


class LoginView(View):
    """
    Handles user authentication and session creation.
    """
    template_name = 'accounts/login.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('articles:home')
        form = LoginForm()
        return render(request, self.template_name, {
            'form': form,
            'next': request.GET.get('next', '')
        })

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('articles:home')

        form = LoginForm(request.POST)
        next_url = request.POST.get('next') or request.GET.get('next') or 'articles:home'

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = self.auth_service.authenticate_user(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'خوش آمدید، {user.username}!')
                if next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('articles:home')
            else:
                form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است.')

        return render(request, self.template_name, {
            'form': form,
            'next': next_url
        })
