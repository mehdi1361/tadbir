# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, Location, Human, Document
from states.models import City, State
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Bank(Base):
    name = models.CharField(_('bank name'), max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        db_table = 'banks'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ManagementAreas(Base, Location):
    name = models.CharField(_('area name'), max_length=100)
    bank = models.ForeignKey(Bank, verbose_name=_('bank'), related_name='areas', on_delete=models.CASCADE)
    state = models.ForeignKey(State, verbose_name=_('state'), related_name='areas_state', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        db_table = 'areas'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Branch(Base, Location):
    name = models.CharField(_('branch name'), max_length=100)
    area = models.ForeignKey(ManagementAreas, verbose_name=_('area'), related_name='branches',
                             on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('city'), related_name='areas', on_delete=models.CASCADE)
    postal_code = models.CharField(_('کد شعبه'), max_length=20, default=None, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('branch')
        verbose_name_plural = _('branch')
        db_table = 'branches'

    def __str__(self):
        return '{}-{}-{}'.format(self.area, self.city, self.name)


@python_2_unicode_compatible
class File(Base):
    STATUS = (
        (u"سررسید گذشته", u"سر رسید گذشته"),
        (u"معوق", u"معوق"),
        (u"مشکوک الوصول", u"مشکوک الوصول")
    )

    TYPE = (
        ('جعاله', 'جعاله'),
        ('اعتباری خرید کالا', 'اعتباری خرید کالا'),
        ('خرید خودرو', 'خرید خودرو'),
    )
    file_code = models.CharField(_(u'کد پرونده'), max_length=200, unique=True)
    contract_code = models.CharField(_(u'شماره قرارداد'), max_length=200, unique=True)
    main_deposit = models.PositiveIntegerField(_(u'اصل مبلغ بدهی'), default=100)
    nc_deposit = models.PositiveIntegerField(_(u'وجه التزام'), default=100)
    so_deposit = models.PositiveIntegerField(_(u'سود'), default=100)
    cost_proceeding = models.PositiveIntegerField(_(u'هزینه دادرسی'), default=100)
    branch = models.ForeignKey(Branch, verbose_name=_(u'شعبه'))
    persian_date_refrence = models.CharField(_(u'تاریخ ارجاع'), max_length=10, default=None, null=True)
    persian_normal_date_refrence = models.CharField(_(u'تاریخ ارجاع'), max_length=10, default=None, null=True)
    status = models.CharField(_(u'وضعیت'), max_length=20, choices=STATUS, default='مشکوک')
    file_type = models.CharField(_('نوع قرارداد'), max_length=50, choices=TYPE, default='جعاله')

    class Meta:
        ordering = ['file_code']
        verbose_name = _('file')
        verbose_name_plural = _('files')
        db_table = 'files'

    def __str__(self):
        return "{}".format(self.file_code)


@python_2_unicode_compatible
class Person(Base, Human):
    file = models.ManyToManyField(File, through='PersonHuman', verbose_name=_('شخص'), related_name='persons')

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'persons'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class PersonHuman(Base):
    TYPE = (
        ('مدیون', 'مدیون'),
        ('ضامن', 'ضامن'),
        ('منفرقه', 'متفرقه'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='file_persons')
    person = models.ForeignKey(Person, verbose_name=_('شخص'), related_name='file_persons')
    relation_type = models.CharField(_('ارتباط'), max_length=10, default='مدیون', choices=TYPE)

    class Meta:
        verbose_name = _('person_human')
        verbose_name_plural = _('person_humans')
        db_table = 'person_humans'

    def __str__(self):
        return "{}-{} {}".format(self.file.file_code, self.person.first_name, self.person.last_name)


class Assurance(Base, Document):
    pass




