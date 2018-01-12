from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, Location
from states.models import City, State


class Bank(Base):
    name = models.CharField(_('bank name'), max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('bank')
        verbose_name_plural = _('banks')
        db_table = 'banks'

    def __str__(self):
        return self.name


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


class Branch(Base, Location):
    name = models.CharField(_('branch name'), max_length=100)
    area = models.ForeignKey(ManagementAreas, verbose_name=_('area'), related_name='branches',
                             on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_('city'), related_name='areas', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = _('branch')
        verbose_name_plural = _('branch')
        db_table = 'branches'

    def __str__(self):
        return self.name


class File(Base):
    STATUS = (
        ('سررسید گذشته', 'سر رسید گذشته'),
        ('معوق', 'معوق'),
        ('مشکوک الوصول', 'مشکوک الوصول')
    )

    file_code = models.CharField(_('کد پرونده'), max_length=200)
    contract_code = models.CharField(_('شماره قرارداد'), max_length=200)
    main_deposit = models.PositiveIntegerField(_('اصل مبلغ بدهی'), default=100)
    end_deposit = models.PositiveIntegerField(_('میزان خواسته'), default=100)
    cost_proceeding = models.PositiveIntegerField(_('هزینه دادرسی'), default=100)
    branch = models.ForeignKey(Branch, verbose_name=_('شعبه'))
    persian_date_refrence = models.CharField(_('تاریخ ارجاع'), max_length=10, default=None, null=True)
    persian_normal_date_refrence = models.CharField(_('تاریخ ارجاع'), max_length=10, default=None, null=True)
    status = models.CharField(_('وضعیت'), max_length=20, choices=STATUS, default='مشکوک')

    class Meta:
        ordering = ['file_code']
        verbose_name = _('file')
        verbose_name_plural = _('files')
        db_table = 'files'

    def __str__(self):
        return "{}".format(self.file_code)




