from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, FormView
from django.http import HttpResponse, HttpResponseRedirect

from gps.models import GpsNode, GpsNodeMetrics

class GpsNodeCreate(CreateView):
    model = GpsNode
    fields = ['ident', 'user']
    success_url = reverse_lazy('gps:index')

class GpsNodeDelete(DeleteView):
    model = GpsNode
    success_url = reverse_lazy('gps:index')

# Create your views here.
class GpsNodesListView(ListView):
    model = GpsNode
    template_name = 'gps/gpsnode_list.html'
    context_object_name = 'nodes'

    def get_queryset(self):
        return GpsNode.objects.order_by('-lastActive')

class GpsNodeDetailView(DetailView):
    model = GpsNode
    template_name = 'gps/gpsnode_detail.html'

"""
def GpsNodeUpdateView(request, pk):
    from django.http import HttpResponse
    return HttpResponse('Update not implemented yet for GpsNode %r.' % pk)

"""
from django.forms import ModelForm

class MetricsForm(ModelForm):
    class Meta:
        model = GpsNodeMetrics
        fields = ['vin', 'vinCached', 'latitude', 'longitude',
                  'accuracy', 'speed', 'altitude', 'nsTimestamp',
                  'bearing']
        """
        fields = ['node', 'vin', 'vinCached', 
                  'latitude', 'longitude', 'accuracy',
                  'speed', 'altitude', 'nsTimestamp',
                  'bearing']
        """

from django.http import HttpResponse
def GpsNodeUpdateView(request, pk=None):
    node = get_object_or_404(GpsNode, pk=pk)
    if request.method == 'POST':
        form = MetricsForm(request.POST)
        if form.is_valid():
            print 'MetricsForm is valid'
            c = form.save(commit=False)
            c.node = node
            c.save()
            url = '/gps/%s/detail' % pk
            return HttpResponseRedirect(url)
            #return render(request, 'gps/gpsnode_detail.html', 
            #                    {'gpsnode' : node})
        else:
            return render(request, 'gps/gpsnode_update.html',
                            {'node' : node, 'pk' : pk, 'form' : form,
                             'error_message' : 'Invalid form submitted'})
    else:
        form = MetricsForm()
        return render(request, 'gps/gpsnode_update.html', 
                        {'node' : node, 'pk' : pk, 'form' : form})

""""
class GpsNodeUpdateView(FormView):
    form_class = MetricsForm
    #success_url = "gps:detail"
    template_name = 'gps/gpsnode_update.html'

    def get_context_data(self, **kwargs):
        data = super(GpsNodeUpdateView, self).get_context_data(**kwargs)
        print 'updateView form arg %r' % data
        import pdb; pdb.set_trace()
        myform = data['form']
        myview = data['view']
        #mynode = myform.node
        #mynode = getattr(myform, 'node', None)
        print 'root node: %r, view %r' % (myform, myview)
        return data

    def get_success_url(self):
        return reverse('gps:update', kwargs={'pk':self.id})
"""
