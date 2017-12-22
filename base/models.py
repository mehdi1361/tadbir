from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Base(models.Model):
    created_at = models.DateTimeField(_('created date'), auto_now_add=True)
    update_at = models.DateTimeField(_('updated date'), auto_now=True)

    class Meta:
        abstract = True


class BasePerson(models.Model):
    GENDER = (
        ('male', _('male')),
        ('female', _('female'))
    )
    first_name = models.CharField(_('first name'), max_length=200)
    last_name = models.CharField(_('last_name'), max_length=200)
    father_name = models.CharField(_('father_name'), max_length=200)
    national_code = models.CharField(_('national code'), max_length=20)
    gender = models.CharField(_('gender'), max_length=20, choices=GENDER)

    class Meta:
        abstract = True


class BaseLocation(models.Model):
    name = models.CharField(_('location name'), max_length=200)
    address = models.TextField(_('address'), default=None, null=True)
    postal_code = models.CharField(_('postal code'), default=None, null=True)

    class Meta:
        abstract = True
