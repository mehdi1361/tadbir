# -*- coding: utf-8 -*-
import jdatetime

from django.db import models
from bank.models import File, PersonFile
from base.models import Base, Human, Document
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django_jalali.db import models as jmodels
from bank.models import SmsType
from bank.models import ManagementAreas


@python_2_unicode_compatible
class FileManager(models.Manager):
    def get_queryset(self):
            return super(FileManager, self).get_queryset().filter(status='enable')


@python_2_unicode_compatible
class EmployeeFile(Base):
    AUTH_STATUS = (
        ('کارشناس', 'کارشناس'),
        ('وکیل', 'وکیل'),
    )
    STATUS = (
        ('enable', 'فعال'),
        ('disable', 'غیر فعال'),
    )

    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='employees')
    employee = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='files')
    status = models.CharField(_('وضعیت'), max_length=50, default='enable', choices=STATUS)
    auth_status = models.CharField(_('نوع تخصیص'), max_length=50, default='کارشناس', choices=AUTH_STATUS)
    recovery_date = jmodels.jDateField(_('تاریخ ارجاع'), null=True)

    objects = models.Manager()
    files = FileManager()

    class Meta:
        permissions = (
            ('employee_file', 'employee file permissions'),
            ('employee_file_assign', 'assign file to employee'),
        )
        unique_together = ('file', 'employee')
        verbose_name = _('تخصیص پرونده')
        verbose_name_plural = _('تخصیص پرونده')
        db_table = 'employee_files'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class Profile(Base, Human):
    CERTIFICATE = (
        ('کارشناسی حقوق', 'کارشناسی حقوق'),
        ('کارشناسی ارشد حقوق', 'کارشناسی ارشد حقوق'),
        ('کارشناسی ارشد حقوق', 'کارشناسی ارشد حقوق'),
        ('کارشناسی الکترونیک', 'کارشناسی الکترونیک'),
        ('لیسانس مدیریت', 'لیسانس مدیریت'),
        ('لیسانس صنایع', 'لیسانس صنایع'),
        ('کارشناسی ارشدحقوق جزا', 'کارشناسی ارشدحقوق جزا'),
        ('مدیریت دولتی- مدیریت نیروی انسانی', 'مدیریت دولتی- مدیریت نیروی انسانی'),
    )

    EMP_POST = (
      ('کارشناسی حقوق', 'کارشناسی حقوق'),
      ('کارشناسی ارشد حقوق', 'کارشناسی ارشد حقوق'),
    )
    user = models.OneToOneField(User, verbose_name=_('پروفایل'), related_name='profile')
    certificate = models.CharField(_('مدرک تحصیلی'), max_length=200, choices=CERTIFICATE, default='کارشناسی حقوق', null=True)
    employee_post = models.CharField(_('سمت'), max_length=200, choices=EMP_POST, default='کارشناسی حقوق', null=True)

    class Meta:
        permissions = (
            ('edit_profile', 'edit profile'),
        )
        verbose_name = _('پروفایل')
        verbose_name_plural = _('پروفایل کاربران')
        db_table = 'profiles'

    def __str__(self):
        return "{}".format(self.name)


@python_2_unicode_compatible
class FollowUp(Base):
    TYPE = (
        ('call', 'تماس تلفنی'),
        ('meeting', 'مذاکره حضوری'),
        ('law', 'اقدامات قانونی'),
    )

    follow_up_type = models.CharField(_('نوع پیگیری'), max_length=20, choices=TYPE, default='call')
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='follows')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        permissions = (
            ('create_follow', 'create followup for file'),
            ('update_follow', 'update followup for file'),
            ('read_follow', 'read followup for file'),
        )
        verbose_name = _('پیگیری کارشناس')
        verbose_name_plural = _('پیگیری کارشناسان')
        db_table = 'employee_file_folllow_ups'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class SmsCaution(Base):
    STATUS_TYPE = (
        ('در صف ارسال', 'در صف ارسال'),
        ('ارسال شد', 'ارسال شد'),
        ('دریافت شد', 'دریافت شد'),
        ('خطا در زمان ارسال', 'خطا در زمان ارسال'),
    )

    type = models.ForeignKey(SmsType, verbose_name=_('نوع پیامک'), null=True, related_name='sms_cautions')
    mobile_number = models.ForeignKey('PhoneFile', verbose_name=_('شماره تلفن'))
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='sms_cautions')
    status = models.CharField(_('وضعیت'), max_length=100, choices=STATUS_TYPE, default='در صف ارسال')
    description = models.TextField(_('توضیحات'), null=True, default=None)

    class Meta:
        unique_together = ('mobile_number', 'file', 'type')
        verbose_name = _('پیامک کارشناس')
        verbose_name_plural = _('پیامک کارشناسان')
        db_table = 'employee_file_sms_caution'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class PhoneFile(Base):
    phone_number = models.CharField(_('شماره تماس'), max_length=20)
    phone_owner = models.ForeignKey(PersonFile, verbose_name=_('نام شخص'), null=True, related_name='phones')
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='phones')
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
        ('اسناد ضمه ای', 'اسناد ضمه ای'),
        ('قرارداد', 'قرارداد'),
    )

    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='documents')
    type = models.CharField(_('وثایق'), max_length=20, choices=TYPE, default='وثیقه')
    image_upload = models.ImageField(_('تصویر سند'), upload_to='document', null=True)

    class Meta:
        unique_together = ('type', 'file', 'description')
        verbose_name = _('نوع وثایق')
        verbose_name_plural = _('نوع وثایق')
        db_table = 'document_file'

    def __str__(self):
        return self.file.file_code


@python_2_unicode_compatible
class FileReminder(Base):
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='reminders')
    subject = models.CharField(_('موضوع'), max_length=100)
    detail = models.TextField(_('شرح'))
    persian_date = jmodels.jDateField(_('تاریخ'), null=True)

    class Meta:
        verbose_name = _('file_reminder')
        verbose_name_plural = _('file_reminders')
        db_table = 'file_reminders'

    def __str__(self):
        return self.subject


@python_2_unicode_compatible
class FileRecovery(Base):
    RECOVERY_TYPE = (
        ('نقدی', 'نقدی'),
        ('چک', 'چک'),
        ('فروش رهنی', 'فروش رهنی'),
    )
    file = models.ForeignKey(File, verbose_name=_('پرونده'), related_name='recoveries')
    recovery_type = models.CharField(_('نوع وصولی'), max_length=100, choices=RECOVERY_TYPE, default='نقدی')
    value = models.PositiveIntegerField(_('مبلغ وصولی'), default=0)
    value_code = models.CharField(_('شماره سند'), max_length=200, default='0')
    detail = models.TextField(_('شرح'))
    recovery_date = jmodels.jDateField(_('تاریخ'), null=True)
    created_at = jmodels.jDateField(_('تاریخ'), null=True, auto_now_add=True)
    assurance_confirm = models.BooleanField(_('تاییدیه مالی'), default=False)

    class Meta:
        unique_together = ('file', 'recovery_type', 'value_code')
        verbose_name = _('file_recovery')
        verbose_name_plural = _('file_recoveries')
        db_table = 'file_recoveries'

    def __str__(self):
        return self.value_code


@python_2_unicode_compatible
class EmployeePermission(Base):
    PERMISSION_TYPE = (
        ('dashboard', 'داشبورد'),
        ('employee_file', 'پرونده های کارشناسان'),
        ('bank_new', 'ایجاد بانک'),
        ('bank_edit', 'ویرایش بانک'),
        ('bank_list', 'لیست بانک'),
        ('area_new', 'سرپرستی جدید'),
        ('area_edit', 'ویرایش سرپرستی'),
        ('area_list', 'لیست مناطق'),
        ('branch_new', 'شعبه جدید'),
        ('branch_edit', 'ویرایش شعبه'),
        ('branch_list', 'لیست شعب'),
        ('sms_list', 'متن پیامک'),
        ('set_permission', 'تعیین سطح دسترسی'),
        ('file_new', 'پرونده جدید'),
        ('file_edit', 'ویرایش پرونده'),
        ('file_list', 'لیست پرونده ها'),
        ('person_new', 'شخص حقیقی جدید'),
        ('person_edit', 'ویرایش شخص حقیقی'),
        ('office_new', 'شخص حقوقی جدید'),
        ('office_edit', 'ویرایش شخص حقوقی'),
        ('office_list', 'لیست اشخاص حقوقی'),
        ('report_user', 'گزارش عملکرد کارشناسان'),
        ('report_bank', 'گزارش به تفکیک بانک'),
        ('role_access', 'تعیین سطح دسترسی'),
        ('create_employee', 'ایجاد کاربر'),
    )
    employee = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='permissions')
    permission_type = models.CharField(_('دسترسی'), max_length=100, choices=PERMISSION_TYPE, default='dashboard')
    enable = models.BooleanField(_('فعال'), default=False)

    class Meta:
        unique_together = ('permission_type', 'employee')
        verbose_name = _('employee_permission')
        verbose_name_plural = _('employee_permission')
        db_table = 'employee_permission'

    def __str__(self):
        return '{}-{}-{}'.format(self.employee, self.permission_type, self.enable)

    @classmethod
    def has_perm(cls, emp, perm):
        try:
            cls.objects.get(employee=emp, permission_type=perm, enable=True)
            return True
        except cls.DoesNotExist:
            return False


@python_2_unicode_compatible
class Mail(Base):
    subject = models.CharField(_('موضوع'), max_length=250)
    description = models.TextField(_('متن'))

    class Meta:
        verbose_name = _('mail')
        verbose_name_plural = _('mails')
        db_table = 'mails'

    def __str__(self):
        return '{}'.format(self.subject)


@python_2_unicode_compatible
class MailBox(Base):
    from_user = models.ForeignKey(User, verbose_name=_('از'), related_name='send_messages')
    to_user = models.ForeignKey(User, verbose_name=_('به'), related_name='receive_messages')
    mail = models.ForeignKey(Mail, verbose_name=_('نامه'), related_name='inbox')
    star = models.BooleanField(_('نشان گزاری'), default=False)

    class Meta:
        verbose_name = _('mail_box')
        verbose_name_plural = _('mail_boxes')
        db_table = 'mail_boxes'

    def __str__(self):
        return '{}-{}-{}'.format(self.from_user, self.to_user, self.mail)


@python_2_unicode_compatible
class AccessEmployee(Base):
    area = models.ForeignKey(ManagementAreas, verbose_name=_('منطقه'), related_name='access_areas')
    employee = models.ForeignKey(User, verbose_name=_('کاربر'), related_name='users')
    enable = models.BooleanField(_('فعال'), default=False)

    class Meta:
        verbose_name = _('access')
        verbose_name_plural = _('access')
        db_table = 'access'

    def __str__(self):
        return '{}-{}'.format(self.area.name, self.user.profile.name)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        for role in EmployeePermission.PERMISSION_TYPE:
            EmployeePermission.objects.create(employee=instance, permission_type=role[0])

        for area in ManagementAreas.objects.all():
            AccessEmployee.objects.create(employee=instance, area=area)
    instance.profile.save()



