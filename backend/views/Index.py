from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View


class IndexView(View):

    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, 'backend/index.html', {'user': request.user})
