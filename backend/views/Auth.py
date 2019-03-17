from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View


class AuthView(View):
    from backend.forms import LoginForm
    from django.contrib.auth.models import User

    def get(self, request):
        url = request.GET.get('next')
        form = self.LoginForm(initial={'next': url})
        return render(request, 'backend/login.html', {'form': form})

    def post(self, request):
        form = self.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,
                                password=password)
            if user is not None:
                login(request, user)
                url = form.cleaned_data['next']
                return HttpResponseRedirect(url)
        return render(request, 'backend/login.html', {"message": "error"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
