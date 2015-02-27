from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout

from gps.models import GpsNode, GpsNodeMetrics

def appDefault(request):
    """ Root page, default landing page... if already logged in, 
         then redirect to index page, else show login page """
    if request.user.is_authenticated() and request.user.is_active:
        if request.user.is_superuser:
            print 'user %r is superuser' % request.user
            return HttpResponseRedirect('/admin')
        else:
            print 'user %r is regular' % request.user
            #return HttpResponseRedirect('gps:index')
            return HttpResponseRedirect('/gps')
    print 'Anonymous user or inactive user.. redirect to login page'
    # TODO
    #return HttpResponseRedirect(request, 'gps:login')
    return HttpResponseRedirect('/gps/login')

def appLogin(request):
   """ Handles application login """
   error_msg = ''
   if request.method == 'POST':
       myuser = request.POST['your_name']
       mypasswd = request.POST['your_passwd']
       print 'username %s, password %s' % (myuser, mypasswd)  
       user = authenticate(username=myuser, password=mypasswd)
       if user is not None:
           if user.is_active:
               print "User is valid, active"
               login(request, user)
               return HttpResponseRedirect('/gps')
           else:
               error_msg="User account disabled"
       else:
           error_msg="User/password combination is not correct"
   return render(request, 'gps/gpsnode_login.html', 
                   {'error_message' : error_msg})

def appLogout(request):
    """ Handles application logout """
    if request.method == 'POST':
       logout(request)
       return render(request, 'gps/gpsnode_login.html', {})
    return render(request, 'gps/gpsnode_confirm_logout.html', {})

class GpsNodeCreate(CreateView):
    model = GpsNode
    fields = ['ident']
    success_url = reverse_lazy('gps:index')
    template_name_suffix = '_add_form'

    def form_valid(self, form):
        # bind user into newly created node
        node = form.instance
        user = self.request.user
        print 'request user %r' % self.request.user
        if not user:
            raise Http404('Anonymous user cannot modify account. Please login and retry.')
        node.user = user
        return super(GpsNodeCreate, self).form_valid(form)

class GpsNodeUpdate(UpdateView):
    model = GpsNode
    fields = ['ident']
    success_url = reverse_lazy('gps:index')
    template_name_suffix = '_mod_form'

    def form_valid(self, form):
        # bind user into newly created node
        node = form.instance
        user = self.request.user
        print 'request user %r with pk=%r' % (user, user.id)
        if not user:
            raise Http404('Anonymous user cannot modify account. Please login and retry.')
        node.user = user
        return super(GpsNodeUpdate, self).form_valid(form)


class GpsNodeDelete(DeleteView):
    model = GpsNode
    success_url = reverse_lazy('gps:index')

    def get_object(self, queryset=None):
        obj = super(GpsNodeDelete, self).get_object(queryset)
        if not obj.user.id == self.request.user.id:
            raise Http404('Sorry..user has no permission to delete this record.')
        return obj 

class GpsNodesListView(ListView):
    model = GpsNode
    template_name = 'gps/gpsnode_list.html'
    context_object_name = 'nodes'

    def get_queryset(self):
        return GpsNode.objects.filter(user=self.request.user.id)

class GpsNodeDetailView(DetailView):
    model = GpsNode
    template_name = 'gps/gpsnode_detail.html'


class MetricsForm(ModelForm):
    class Meta:
        model = GpsNodeMetrics
        fields = ['vin', 'vinCached', 'latitude', 'longitude',
                  'accuracy', 'speed', 'altitude', 'nsTimestamp',
                  'bearing']

def GpsNodeMetricsAdd(request, pk=None):
    node = get_object_or_404(GpsNode, pk=pk)
    if request.method == 'POST':
        form = MetricsForm(request.POST)
        if form.is_valid() and node.user.id == request.user.id:
            print 'MetricsForm is valid'
            c = form.save(commit=False)
            c.node = node
            c.save()
            url = '/gps/%s/detail' % pk
            return HttpResponseRedirect(url)
        else:
            return render(request, 'gps/gpsnode_update.html',
                            {'node' : node, 'pk' : pk, 'form' : form,
                             'error_message' : 'Invalid form submitted'})
    elif node.user.id  != request.user.id:
        print 'user %r has no record for this node - %r' % (request.user, node.user)
        raise Http404('User has no such record.')
    else:
        form = MetricsForm()
        return render(request, 'gps/gpsnode_update.html', 
                        {'node' : node, 'pk' : pk, 'form' : form})
