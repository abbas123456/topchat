import json
import uuid

from django.core import urlresolvers, serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, hashers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views import generic
from rest_framework import generics, permissions
from account.serializers import UserSearchSerializer, AuthenticationTokenSerializer
from account.models import AuthenticationToken
from account.forms import UserForm


class UserCreateView(generic.CreateView):
    form_class = UserForm
    model = User
    template_name = 'account/user_form.html'

    def get(self, request, *args, **kwargs):
        form = UserForm()
        if request.user.is_authenticated():
            return HttpResponseRedirect(urlresolvers.reverse('home'))
        return render_to_response(self.template_name, {'form': form},
                                  context_instance=RequestContext(request))

    def form_valid(self, form):
        username = form.instance.username
        password = form.instance.password
        User.objects.create_user(username=username, password=password)
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is not None:
            login(self.request, authenticated_user)
        return HttpResponseRedirect(urlresolvers.reverse('dashboard_general'))


class UserDetailView(generic.DetailView):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(urlresolvers.reverse('dashboard_general'))


class GenerateTokenView(generic.TemplateView):
    
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'username' in request.POST and 'password' in request.POST:
            user, created = User.objects.get_or_create(username=request.POST['username'])
            if created:
                user.set_password(request.POST['password'])
                user.save()
                authentication_token = self.generate_token(user)
            else:
                if hashers.check_password(request.POST['password'], user.password):
                    authentication_token = self.generate_token(user)
                else:
                    authentication_token = AuthenticationToken()
        else:
            authentication_token = AuthenticationToken()
        context['authentication_token'] = serializers.serialize('json', [ authentication_token,])
        return self.render_to_response(context)

    def generate_token(self, user):
        return AuthenticationToken.objects.create(user=user,token_string=uuid.uuid4())

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(json.dumps(context),**response_kwargs)


##############################################################################
##
## REST API VIEWS
##
##############################################################################


class UserAuthenticationTokenView(generics.RetrieveAPIView):
    model = AuthenticationToken
    serializer_class = AuthenticationTokenSerializer
    slug_url_kwarg = 'token_string'
    slug_field = 'token_string'


class UserAuthenticationTokenDeleteView(generics.DestroyAPIView):
    model = AuthenticationToken
    slug_url_kwarg = 'token_string'
    slug_field = 'token_string'


class UserListApiView(generics.ListAPIView):
    model = User
    serializer_class = UserSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.exclude(username='admin').exclude(username='anonymous')

    def filter_queryset(self, queryset):
        search_query = self.kwargs['search_query']
        limit = self.kwargs['limit']
        users = queryset.filter(username__icontains=search_query)
        return users[0:limit]
