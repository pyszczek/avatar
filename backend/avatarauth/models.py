from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import models as auth_models
from django.dispatch import receiver

from . import utils


class UserGroup(Enum):
    SYSTEM_ADMINISTRATOR = 'SYSTEM_ADMINISTRATOR'
    USER = 'USER'


class UserManager(auth_models.UserManager):
    def activated(self):
        return self.filter(is_active=True)

    def not_activated(self):
        return self.filter(is_active=False)

    def get_by_uuid(self, user_uuid: str, otp=None, is_active=True):
        if otp:
            return self.get(uuid=user_uuid, otp=otp, is_active=is_active)
        return self.get(uuid=user_uuid, is_active=is_active)


class User(auth_models.AbstractUser):
    uuid = models.CharField(max_length=200, unique=True, db_index=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    secret_key = models.CharField(max_length=255, verbose_name=_('Secret key'))
    otp = models.CharField(max_length=255, verbose_name=_('OTP'))

    objects = UserManager()

    @property
    def groups_names(self):
        return [group.name for group in self.groups.all()]

    def has_group(self, group_name):
        return self.groups.filter(name=group_name).exists()

    def activate(self):
        self.is_active = True
        self.save()

    def __str__(self):
        return self.uuid

    class PasswordResetTokenInvalid(Exception):
        pass


@receiver(models.signals.pre_save, sender=User)
def user_pre_save_callback(sender, **kwargs):
    instance: User = kwargs['instance']

    if not instance.uuid:
        uuid_val = str(utils.generate_uuid())
        instance.uuid = uuid_val
        instance.username = uuid_val

    if not instance.secret_key:
        instance.secret_key = utils.get_random_string(length=128)

    if not instance.otp:
        instance.otp = utils.get_random_string(length=6)
