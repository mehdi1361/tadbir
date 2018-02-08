# -*- coding: utf-8 -*-
from django.db import models
from bank.models import File
from base.models import Base, Human
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FileManager(models.Manager):
    def get_queryset(self):
            return super(FileManager, self).get_queryset().filter(status='enable')


@python_2_unicode_compatible
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


@python_2_unicode_compatible
class Profile(Base, Human):
    user = models.OneToOneField(User, verbose_name=_('پروفایل'), related_name='profile')

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        db_table = 'profiles'

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@python_2_unicode_compatible
class FollowUp(Base):
    TYPE = (
        ('call', 'تماس تلفنی'),
        ('meeting', 'مذاکره حضوری'),
    )

    follow_up_type = models.CharField(_('نوع پیگیری'), max_length=20, choices=TYPE, default='call')
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='follows')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        verbose_name = _('employee_file_folllow_up')
        verbose_name_plural = _('employee_file_folllow_ups')
        db_table = 'employee_file_folllow_ups'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class SmsCaution(Base):
    TYPE = (
        ('caution1', 'اخطار اول'),
        ('caution2', 'اخطار دوم'),
        ('caution3', 'اخطار سوم'),
    )

    caution_type = models.CharField(_('نوع اخطار'), max_length=20, choices=TYPE, default='caution1')
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='sms_cautions')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        verbose_name = _('employee_file_sms_caution')
        verbose_name_plural = _('employee_file_sms_caution')
        db_table = 'employee_file_sms_caution'

    def __str__(self):
        return self.file.file_code


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
