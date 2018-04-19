from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from .forms import AccountLoginForm
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import login, logout
from django.conf import settings
from analytics.signals import user_logged_in_signal, user_logged_out_signal


class AccountLoginView(LoginView):
    """
    Login form
    """
    form_class = AccountLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('console:index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super(AccountLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        user = self.request.user
        request = self.request
        # calling analytics signals
        user_logged_in_signal.send(user.__class__, instance=user, request=request)
        return redirect(self.get_success_url())


class AccountLogoutView(TemplateView):
    """
    Delete all session
    """
    logout_redirect = settings.LOGOUT_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        # user_logged_in_signal.send(user.__class__, instance=user, request=request)
        logout(request)
        return redirect(self.logout_redirect)
