from django.db import models
from bank.models import File
from base.models import Base, Human
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class FileManager(models.Manager):
    def get_queryset(self):
            return super(FileManager, self).get_queryset().filter(status='enable')


class EmployeeFile(Base):
    STATUS = (
        ('enable', 'enable'),
        ('disable', 'disable'),
    )

    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='employees')
    employee = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='files')
    status = models.CharField(_('وضعیت'), max_length=50, default='enable', choices=STATUS)

    objects = models.Manager()
    files = FileManager()

    class Meta:
        verbose_name = _('employee_file')
        verbose_name_plural = _('employee_files')
        db_table = 'employee_files'

    def __str__(self):
        return self.file.file_code


class Profile(Base, Human):
    user = models.OneToOneField(User, verbose_name=_('پروفایل'), related_name='profile')

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profiles'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


