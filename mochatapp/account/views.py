from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView
from account.forms import UserForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login

class UserCreateView(CreateView):
    form_class = UserForm
    model = User
    template_name = 'account/user_form.html'
    
    def get(self, request, *args, **kwargs):
        form = UserForm()
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))
    
    def form_valid(self, form):
        username = form.instance.username
        password = form.instance.password
        user = User.objects.create_user(username=username, password=password)
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login(self.request, authenticated_user)
        return HttpResponseRedirect(reverse('home'))

class UserDetailView(DetailView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('home'))
