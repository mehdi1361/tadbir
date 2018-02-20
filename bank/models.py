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
    file = models.ManyToManyField(File, through='PersonFile', verbose_name=_('شخص'), related_name='persons')

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'persons'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Office(Base, Location):
    name = models.CharField(_('نام شرکت'), max_length=200)
    city = models.ForeignKey(City, verbose_name=_('نام شهر'),null=True)
    register_number = models.PositiveIntegerField(_('شماره ثبت'), unique=True)

    class Meta:
        ordering = ['register_number']
        verbose_name = _('person_office')
        verbose_name_plural = _('person_offices')
        db_table = 'person_offices'

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class FileOffice(Base):
    TYPE = (
        ('مدیون', 'مدیون'),
        ('ضامن', 'ضامن'),
        ('منفرقه', 'متفرقه'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='related_office')
    office = models.ForeignKey(Office, verbose_name=_('شرکت'), related_name='related_office')
    relation_type = models.CharField(_('ارتباط'), max_length=10, default='مدیون', choices=TYPE)

    class Meta:
        unique_together = ['file', 'office']
        verbose_name = _('file_office')
        verbose_name_plural = _('file_offices')
        db_table = 'file_offices'

    def __str__(self):
        return "{}-{}".format(self.file.file_code, self.office.name)


@python_2_unicode_compatible
class PersonFile(Base):
    TYPE = (
        ('مدیون', 'مدیون'),
        ('ضامن', 'ضامن'),
        ('منفرقه', 'متفرقه'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='file_persons')
    person = models.ForeignKey(Person, verbose_name=_('شخص'), related_name='file_persons')
    relation_type = models.CharField(_('ارتباط'), max_length=10, default='مدیون', choices=TYPE)

    class Meta:
        unique_together = ['file', 'person']
        verbose_name = _('person_file')
        verbose_name_plural = _('person_files')
        db_table = 'person_files'

    def __str__(self):
        return "{}-{} {}".format(self.file.file_code, self.person.first_name, self.person.last_name)


@python_2_unicode_compatible
class Assurance(Base, Document):
    TYPE = (
        ('سفته', 'سفته'),
        ('چک', 'چک'),
        ('سند ملکی', 'سند ملکی'),
        ('سند در رهن', 'سند در رهن'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='assurances', default=None)
    assurance_type = models.CharField(_('نوع وثیقه'), max_length=50, choices=TYPE, default='سفته')
    assurance_number = models.CharField(_('شماره سند'), max_length=200, default=0)
    assurance_date = models.CharField(_('تاریخ'), max_length=200, default='')
    assurance_value = models.PositiveIntegerField(_('مبلغ'), default=0)

    class Meta:
        unique_together = ['file', 'assurance_type','assurance_number']
        verbose_name = _('assurance')
        verbose_name_plural = _('assurances')
        db_table = 'assurances'

    def __str__(self):
        return "{}-{}".format(self.assurance_type, self.file)


@python_2_unicode_compatible
class SmsType(Base):
    subject = models.CharField(_('موضوع پیامک'), max_length=50)
    detail = models.TextField(_('مشروح پیامک'))

    class Meta:
        verbose_name = _('sms_type')
        verbose_name_plural = _('sms_types')
        db_table = 'sms_types'

    def __str__(self):
        return "{}".format(self.subject)
