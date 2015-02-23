from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.forms import ModelForm

from gps.models import GpsNode, GpsNodeMetrics

class GpsNodeCreate(CreateView):
    model = GpsNode
    fields = ['ident']
    success_url = reverse_lazy('gps:index')

    def form_valid(self, form):
        # bind user into newly created node
        node = form.instance
        user = self.request.user
        node.user = user
        return super(GpsNodeCreate, self).form_valid(form)

class GpsNodeDelete(DeleteView):
    model = GpsNode
    success_url = reverse_lazy('gps:index')

    def get_object(self, queryset=None):
        obj = super(GpsNodeDelete, self).get_object(queryset)
        if not obj.user == self.request.user:
            raise Http404
        return obj 

class GpsNodesListView(ListView):
    model = GpsNode
    template_name = 'gps/gpsnode_list.html'
    context_object_name = 'nodes'

    def get_queryset(self):
        return GpsNode.objects.filter(user=self.request.user)

class GpsNodeDetailView(DetailView):
    model = GpsNode
    template_name = 'gps/gpsnode_detail.html'


class MetricsForm(ModelForm):
    class Meta:
        model = GpsNodeMetrics
        fields = ['vin', 'vinCached', 'latitude', 'longitude',
                  'accuracy', 'speed', 'altitude', 'nsTimestamp',
                  'bearing']

def GpsNodeUpdateView(request, pk=None):
    node = get_object_or_404(GpsNode, pk=pk)
    if request.method == 'POST':
        form = MetricsForm(request.POST)
        if form.is_valid() and node.user == request.user:
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
    elif node.user != request.user:
        print 'user %r has no record for this node - %r' % (request.user, node.user)
        raise Http404('User has no such record.')
    else:
        form = MetricsForm()
        return render(request, 'gps/gpsnode_update.html', 
                        {'node' : node, 'pk' : pk, 'form' : form})

