from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

from .managers import CustomUserManager
from . import validators

time_now_for_validation = timezone.localtime() + timezone.timedelta(minutes=5)


class User(AbstractBaseUser):
    username = models.CharField('username', max_length=64, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, validators=[EmailValidator])
    first_name = models.CharField('first_name', max_length=64)
    last_name = models.CharField('last_name', max_length=64)
    date_created = models.DateTimeField('created', validators=[MaxValueValidator(limit_value=time_now_for_validation)])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Case(models.Model):
    content = models.CharField('content', max_length=1024, unique=False)
    date_created = models.DateTimeField('created', validators=[
        MaxValueValidator(limit_value=time_now_for_validation)])
    severity = models.IntegerField('severity',
                                   validators=[MinValueValidator(limit_value=1), MaxValueValidator(limit_value=4)])
    is_closed = models.BooleanField('is_closed', default=False)
    user = models.ForeignKey('User', null=False, related_name='user_created', on_delete=models.PROTECT)
    admin_assigned = models.ForeignKey('User', null=True, related_name='admin_assigned', on_delete=models.PROTECT,
                                       validators=[validators.is_admin_validator])


class CaseUpdate(models.Model):
    comment = models.CharField('comment', max_length=1024, unique=False)
    date_created = models.DateTimeField('created', validators=[MaxValueValidator(limit_value=time_now_for_validation)])
    user = models.ForeignKey('User', null=False, on_delete=models.PROTECT)
    case = models.ForeignKey('Case', null=False, on_delete=models.CASCADE)
