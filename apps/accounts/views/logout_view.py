from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


class LogoutView(View):
    """
    Handles logging out the user.
    """
    def post(self, request):
        logout(request)
        messages.info(request, 'با موفقیت از حساب کاربری خود خارج شدید.')
        return redirect('articles:home')

    def get(self, request):
        # Support GET redirect for seamless user navigation
        logout(request)
        messages.info(request, 'با موفقیت از حساب کاربری خود خارج شدید.')
        return redirect('articles:home')
