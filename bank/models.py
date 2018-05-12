# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, Location, Human, Document
from states.models import City, State
from django.utils.encoding import python_2_unicode_compatible
from simple_history.models import HistoricalRecords
from django.db.models import signals


@python_2_unicode_compatible
class Bank(Base):
    name = models.CharField(_('نام بانک'), max_length=100, unique=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('بانک')
        verbose_name_plural = _('بانک ها')
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
        verbose_name = _('منطقه')
        verbose_name_plural = _('مناطق')
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
        verbose_name = _('شعبه')
        verbose_name_plural = _('شعبات')
        db_table = 'branches'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def full_name(self):
        return 'نام شعبه:{},کد شعبه:{},سرپرستی:{}'.format(self.name, self.code, self.area)


@python_2_unicode_compatible
class FileType(Base):
    name = models.CharField(_('نوع پرونده'), max_length=100, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('نوع پرونده')
        verbose_name_plural = _('انواع پرونده')
        db_table = 'file_types'

    def __str__(self):
        return "{}".format(self.name)


class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().order_by('-file_code')


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

    objects = models.Manager()
    ordered = OrderManager()
    history = HistoricalRecords()

    class Meta:
        ordering = ['file_code']
        verbose_name = _('پرونده')
        verbose_name_plural = _('پرونده ها')
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
    file = models.ManyToManyField(File, through='PersonFile', verbose_name=_('پرونده'), related_name='persons')
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']
        verbose_name = _('شخص حقیقی')
        verbose_name_plural = _('اشخاص حقیقی')
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
        verbose_name = _('شخص حقوقی')
        verbose_name_plural = _('اشخاص حقیقی')
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
        verbose_name = _('فرد حقیقی پرونده')
        verbose_name_plural = _('افراد حقیقی پرونده')
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
        verbose_name = _('شخص حقیقی پرونده')
        verbose_name_plural = _('اشخاص حقیقی پرونده')
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
    # assurance_number = models.CharField(_('شماره سند'), max_length=200, default=0)
    assurance_date = models.CharField(_('تاریخ'), max_length=200, default='')
    # assurance_value = models.PositiveIntegerField(_('مبلغ'), default=0)
    history = HistoricalRecords()

    class Meta:
        unique_together = ['file', 'assurance_type']
        verbose_name = _('وثیقه')
        verbose_name_plural = _('وثایق')
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
        verbose_name = _('نوع پیامک')
        verbose_name_plural = _('انواع پیامک')
        db_table = 'sms_types'

    def __str__(self):
        return "{}".format(self.subject)


@python_2_unicode_compatible
class Lawyer(Base, Human):
    mobile_number = models.CharField(_('شماره همراه'), max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = _('وکیل')
        verbose_name_plural = _('وکلا')
        db_table = 'lawyers'

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class LawyerFile(Base):
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='lawyers')
    lawyer = models.ForeignKey(Lawyer, verbose_name=_('وکیل'), related_name='files')
    enable = models.BooleanField(_('فعال'), default=True)
    history = HistoricalRecords()

    objects = models.Manager()
    main_debtor = MainDebtor()

    class Meta:
        unique_together = ['file', 'lawyer']
        verbose_name = _('تخصیص وکیل')
        verbose_name_plural = _('اشخاص حقیقی پرونده')
        db_table = 'lawyer_files'

    @classmethod
    def update_lawyer_file(cls, file, enable=False):
        cls.objects.filter(file=file).update(enable=enable)

    def __str__(self):
        return "{}-{}".format(self.file.file_code, self.lawyer.name)

    def save(self, *args, **kwargs):
        LawyerFile.update_lawyer_file(self.file)
        super(LawyerFile, self).save()


@python_2_unicode_compatible
class FollowLawType(Base):
    type = models.CharField(_('نوع پیگیری'), max_length=100)

    class Meta:
        verbose_name = _('پیگیری حقوقی')
        verbose_name_plural = _('پیگیری های حقوقی')
        db_table = 'follow_low_type'

    def __str__(self):
        return "{}".format(self.type)


@python_2_unicode_compatible
class FollowInLowFile(Base):
    file = models.ForeignKey(File, verbose_name=_('پرونده'))
    follow = models.ForeignKey(FollowLawType, verbose_name=_('پیگیری'))
    enable = models.BooleanField(_('فعال'), default=False)

    class Meta:
        verbose_name = _('پیگیری حقوقی پرونده')
        verbose_name_plural = _('پیگیری های حقوقی پرونده')
        db_table = 'follow_low_file'

    def __str__(self):
        return "{}".format(self.follow.type)


def new_follow_law_type(sender, instance, created, **kwargs):
    if created:
        for file in File.objects.all():
            FollowInLowFile.objects.create(file=file, follow=instance)


def new_file_created(sender, instance, created, **kwargs):
    if created:
        for follow in FollowLawType.objects.all():
            FollowInLowFile.objects.create(file=instance, follow=follow)


# signals.post_save(new_follow_law_type, sender=FollowLawType)
# signals.post_save(new_file_created, sender=File)
