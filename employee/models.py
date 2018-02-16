# -*- coding: utf-8 -*-
from django.db import models
from bank.models import File
from base.models import Base, Human, Document
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from ckeditor.fields import RichTextField


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
    # description = RichTextField(null=True)

    class Meta:
        verbose_name = _('employee_file_sms_caution')
        verbose_name_plural = _('employee_file_sms_caution')
        db_table = 'employee_file_sms_caution'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class PhoneFile(Base):
    PERSON_TYPE = (
        ('مدیون', 'مدیون'),
        ('ضامن', 'ضامن'),
        ('متفرقه', 'متفرقه'),
    )

    TYPE = (
        ('ثابت', 'ثابت'),
        ('همراه', 'همراه'),
    )

    phone_number = models.CharField(_('شماره تماس'), max_length=20)
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='phones')
    person_type = models.CharField(_('مالک'), max_length=10, choices=PERSON_TYPE, default='مدیون')
    type = models.CharField(_('نوع خط'), max_length=10, choices=TYPE, default='ثابت')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        unique_together = ('phone_number', 'file')
        verbose_name = _('employee_phone')
        verbose_name_plural = _('employee_phones')
        db_table = 'employee_phones'

    def __str__(self):
        return self.phone_number


@python_2_unicode_compatible
class AddressFile(Base):
    PERSON_TYPE = (
        ('مدیون', 'مدیون'),
        ('ضامن', 'ضامن'),
        ('متفرقه', 'متفرقه'),
    )

    TYPE = (
        ('ملکی', 'ملکی'),
        ('استیجاری', 'استیجاری'),
        ('رهنی', 'رهنی'),
    )

    address = models.TextField(_('آدرس'))
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='addresses')
    person_type = models.CharField(_('مالک'), max_length=10, choices=PERSON_TYPE, default='مدیون')
    type = models.CharField(_('نوع مالکیت'), max_length=10, choices=TYPE, default='ملکی')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        unique_together = ('address', 'file')
        verbose_name = _('employee_address')
        verbose_name_plural = _('employee_addresses')
        db_table = 'employee_addresses'

    def __str__(self):
        return self.address


@python_2_unicode_compatible
class DocumentFile(Base, Document):

    TYPE = (
        ('وثیقه', 'وثیقه'),
        ('ضمانی', 'ضمانی'),
        ('متفرقه', 'متفرقه'),
    )

    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='documents')
    type = models.CharField(_('نوع مالکیت'), max_length=10, choices=TYPE, default='وثیقه')
    image_upload = models.ImageField(_('تصویر سند'), upload_to='document', null=True)

    class Meta:
        unique_together = ('type', 'file', 'description')
        verbose_name = _('document_file')
        verbose_name_plural = _('document_file')
        db_table = 'document_file'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class FileReminder(Base):
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='reminders')
    subject = models.CharField(_('موضوع'), max_length=100)
    detail = models.TextField(_('شرح'))

    class Meta:
        verbose_name = _('file_reminder')
        verbose_name_plural = _('file_reminders')
        db_table = 'file_reminders'

    def __str__(self):
        return self.subject


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



