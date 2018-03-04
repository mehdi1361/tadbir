from django.db import models
from base.models import Base
from django.utils.translation import ugettext_lazy as _


class State(Base):
    name = models.CharField(_('state name'), max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = _('state')
        verbose_name_plural = _('states')
        db_table = 'states'

    def __str__(self):
        return self.name


class City(Base):
    name = models.CharField(_('city name'), max_length=50)
    state = models.ForeignKey(State, verbose_name=_('state'),
                              related_name='cities', default=None)

    class Meta:
        ordering = ['name']
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        db_table = 'cities'

    def __str__(self):
        return self.name
