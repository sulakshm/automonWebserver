from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

import datetime

# Create your models here.
class GpsNode(models.Model):
    """ Define a GpsNode that collects data for a user """
    user = models.ForeignKey(User)
    ident = models.CharField(max_length=48)
    created = models.DateTimeField('Created', auto_now_add=True)
    lastActive = models.DateTimeField('LastActive', auto_now=True)

    def __unicode__(self):
        return 'GpsNode#'+self.ident

    def was_active_recently(self):
        """ check if lastActive timestamp within last 3 hour period """
        now = timezone.now()
        return now - datetime.timedelta(hours=3) <= self.lastActive 

    def get_absolute_url(self):
        return reverse('index', kwargs={'pk':self.pk})

class GpsNodeMetrics(models.Model):
    """ Define a GpsNodeMetrics attributes for metrics collected """
    node = models.ForeignKey(GpsNode)
    """ Define metrics below from node """
    vin = models.CharField(max_length=32, null=True, blank=True)
    vinCached =  models.NullBooleanField(default=None)
    latitude = models.DecimalField(max_digits=14, decimal_places=12)
    longitude = models.DecimalField(max_digits=14, decimal_places=12)
    accuracy = models.FloatField()
    speed = models.FloatField()
    altitude = models.FloatField()
    nsTimestamp = models.BigIntegerField()
    bearing = models.FloatField() 

    def __unicode__(self):
        return 'GpsNodeMetrics@'+str(self.nsTimestamp)

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:
            fname = f.name        
            try :
                value = getattr(self, fname)
            except User.DoesNotExist:
                value = None

            if f.name not in ('id', 'node'):
                fields.append(
                  {
                   'label':f.verbose_name, 
                   'name':f.name, 
                   'value':value,
                  }
                )
        return fields

