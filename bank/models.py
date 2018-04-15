# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, Location, Human, Document
from states.models import City, State
from django.utils.encoding import python_2_unicode_compatible
from simple_history.models import HistoricalRecords


@python_2_unicode_compatible
class Bank(Base):
    name = models.CharField(_('bank name'), max_length=100, unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        db_table = 'banks'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ManagementAreas(Base, Location):
    name = models.CharField(_('نام سرپرستی'), max_length=100)
    bank = models.ForeignKey(Bank, verbose_name=_('بانک'), related_name='areas', on_delete=models.CASCADE)
    state = models.ForeignKey(State, verbose_name=_('استان'), related_name='areas_state', on_delete=models.CASCADE)
    status = models.BooleanField(_('وضعیت'), default=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        db_table = 'areas'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Branch(Base, Location):
    name = models.CharField(_('نام شعبه'), max_length=100)
    code = models.CharField(_('کد شعبه'), max_length=100, null=True)
    area = models.ForeignKey(ManagementAreas, verbose_name=_('سرپرستی'), related_name='branches',
                             on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('شهر'), related_name='areas', on_delete=models.CASCADE)
    postal_code = models.CharField(_('کد شعبه'), max_length=20, default=None, null=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('branch')
        verbose_name_plural = _('branch')
        db_table = 'branches'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def full_name(self):
        return 'نام شعبه:{},کد شعبه:{},سرپرستی:{}'.format(self.name, self.code, self.area)


@python_2_unicode_compatible
class FileType(Base):
    name = models.CharField(_('نوع فایل'), max_length=100, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('file_types')
        verbose_name_plural = _('file_types')
        db_table = 'file_types'

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class File(Base):
    STATUS = (
        (u"سررسید گذشته", u"سر رسید گذشته"),
        (u"معوق", u"معوق"),
        (u"مشکوک الوصول", u"مشکوک الوصول")
    )

    TYPE = (
        (' جعاله', 'جعاله'),
        ('اعتباری خرید کالا', 'اعتباری خرید کالا'),
        ('خرید خودرو', 'خرید خودرو'),
    )

    ASSURANCE_TYPE = (
        ('خرد', 'خرد'),
        ('متوسط', 'متوسط'),
        ('کلان', 'کلان'),
    )

    STATE_TYPE = (
        ('در حال پیگیری', 'در حال پیگیری'),
        ('عودت', 'عودت'),
        ('تسویه حساب', 'تسویه حساب'),
    )

    file_code = models.CharField(_(u'کد پرونده'), max_length=200, unique=True)
    contract_code = models.CharField(_(u'شماره قرارداد'), max_length=200, null=True)
    main_deposit = models.BigIntegerField(_(u'اصل مبلغ بدهی'), default=100)
    nc_deposit = models.BigIntegerField(_(u'وجه التزام'), default=100)
    so_deposit = models.BigIntegerField(_(u'سود'), default=100)
    cost_proceeding = models.BigIntegerField(_(u'هزینه دادرسی'), default=100)
    branch = models.ForeignKey(Branch, verbose_name=_(u'شعبه'), related_name='files')
    persian_date_refrence = models.CharField(_(u'تاریخ ارجاع'), max_length=10, default=None, null=True)
    persian_normal_date_refrence = models.CharField(_(u'تاریخ ارجاع'), max_length=10, default=None, null=True)
    status = models.CharField(_(u'وضعیت'), max_length=20, choices=STATUS, default='مشکوک')
    # file_type = models.CharField(_('نوع قرارداد'), max_length=50, choices=TYPE, default='جعاله')
    file_type = models.ForeignKey(FileType, verbose_name=_('نوع پرونده'), null=True)
    states = models.CharField(_('وضعیت'), max_length=50, choices=STATE_TYPE, default='در حال پیگیری')
    history = HistoricalRecords()

    class Meta:
        ordering = ['file_code']
        verbose_name = _('file')
        verbose_name_plural = _('files')
        db_table = 'files'

    def __str__(self):
        return "{}".format(self.file_code)

    @property
    def assurance(self):
        if self.main_deposit < 10000000:
            return 'خرد'

        if 10000000 < self.main_deposit < 1000000000:
            return 'متوسط'

        if self.main_deposit > 1000000000:
            return 'کلان'

    @property
    def person_list(self):
        person_str = ''
        for person in self.file_persons.filter(relation_type='مدیون'):
            person_str += '{}'.format(person.person.full_name)

        return person_str

    @property
    def offices(self):
        office_str = ''
        for office in self.related_office.filter(relation_type='مدیون'):
            office_str += '{}'.format(office.office.name)

        return office_str


@python_2_unicode_compatible
class Person(Base, Human):
    name = models.CharField(_('نام و نام خانوادگی'), max_length=200, unique=True, default='')
    file = models.ManyToManyField(File, through='PersonFile', verbose_name=_('شخص'), related_name='persons')
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        db_table = 'persons'

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class Office(Base, Location):
    name = models.CharField(_('نام شرکت'), max_length=200, unique=True)
    city = models.ForeignKey(City, verbose_name=_('نام شهر'),null=True)
    register_number = models.PositiveIntegerField(_('شماره ثبت'), null=True)
    history = HistoricalRecords()

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
    description = models.TextField(_('توضیحات'), null=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ['file', 'office']
        verbose_name = _('file_office')
        verbose_name_plural = _('file_offices')
        db_table = 'file_offices'

    def __str__(self):
        return "{}-{}".format(self.file.file_code, self.office.name)


class MainDebtor(models.Manager):
    def get_queryset(self):
        return super(MainDebtor, self).get_queryset().filter(relation_type='مدیون')


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
    history = HistoricalRecords()

    objects = models.Manager()
    main_debtor = MainDebtor()

    class Meta:
        unique_together = ['file', 'person']
        verbose_name = _('person_file')
        verbose_name_plural = _('person_files')
        db_table = 'person_files'

    def __str__(self):
        return "{}-{}".format(self.file.file_code, self.person.name)


@python_2_unicode_compatible
class Assurance(Base, Document):
    TYPE = (
        ('سند رهنی', 'سند رهنی'),
        ('سفته', 'سفته'),
        ('چک', 'چک'),
        ('قرارداد لازم الاجرا', 'قرارداد لازم الاجرا'),
        ('ضمانت نامه', 'ضمانت نامه'),
        ('کسر از حقوق', 'کسر از حقوق'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='assurances', default=None)
    assurance_type = models.CharField(_('نوع وثیقه'), max_length=50, choices=TYPE, default='سفته')
    assurance_number = models.CharField(_('شماره سند'), max_length=200, default=0)
    assurance_date = models.CharField(_('تاریخ'), max_length=200, default='')
    assurance_value = models.PositiveIntegerField(_('مبلغ'), default=0)
    history = HistoricalRecords()

    class Meta:
        unique_together = ['file', 'assurance_type','assurance_number']
        verbose_name = _('assurance')
        verbose_name_plural = _('assurances')
        db_table = 'assurances'

    def __str__(self):
        return "{}-{}".format(self.assurance_type, self.file)


@python_2_unicode_compatible
class SmsType(Base):
    subject = models.CharField(_('موضوع پیامک'), max_length=50, unique=True)
    detail = models.TextField(_('مشروح پیامک'))
    enable = models.BooleanField(_('فعال'), default=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('sms_type')
        verbose_name_plural = _('sms_types')
        db_table = 'sms_types'

    def __str__(self):
        return "{}".format(self.subject)
