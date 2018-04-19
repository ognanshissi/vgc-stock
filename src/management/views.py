from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomepageView(TemplateView):
    template_name = 'default/index.html'

    login_path = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        user_ = request.user
        if user_.is_authenticated is True:
            return render(request, self.template_name)
        else:
            return redirect(self.login_path)
