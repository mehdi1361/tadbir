from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from base.models import Base
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


@python_2_unicode_compatible
class PersonDailyReport(Base):
    count_file = models.PositiveIntegerField(_('تعداد کل پرونده'), default=0)
    value_file = models.PositiveIntegerField(_('مبلغ کل پرونده'), default=0)
    count_file_daily = models.PositiveIntegerField(_('تعداد پرونده های ارجاعی'), default=0)
    value_file_daily = models.PositiveIntegerField(_('مبلغ پرونده های ارجاعی'), default=0)
    count_file_recovery = models.PositiveIntegerField(_('تعداد پرونده های تسویه'), default=0)
    value_file_recovery = models.PositiveIntegerField(_('مبلغ پرونده های تسویه'), default=0)
    value_recovery = models.PositiveIntegerField(_('مبلغ کل وصولی روز'), default=0)
    count_file_peygiri = models.PositiveIntegerField(_('تعداد پیگیری های روز'), default=0)
    persian_date = jmodels.jDateField(_('تاریخ'), null=True)
    user = models.ForeignKey(User, verbose_name=_('پرسنل'))

    class Meta:
        unique_together = ('user', 'persian_date')
        verbose_name = _('person_daily_report')
        verbose_name_plural = _('persons_daily_report')
        db_table = 'persons_daily_report'

    def __str__(self):
        return '{}-{}'.format(self.user.useername, self.count_file)
