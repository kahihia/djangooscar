from django.conf import settings
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

# Create your models here.
from oscar.models.fields import PhoneNumberField

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Profile(models.Model):
    """
    """
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='profile', verbose_name=_("Profile"))
    home_address = models.CharField(_('Home Address'), max_legnth=255, blank=True)
    mobile_phone = PhoneNumberField(_('Mobile Phone'), blank=True, null=True)
    birth = models.CharField(_('Birthday'), blank=True, null=True)
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
    )
    gender = models.IntegerField(_('Gender'), choices=GENDER_CHOICES, blank=True, null=True)
    college = models.CharField(_('College'), max_length=255, blank=True, null=True)
    hometown = models.CharField(_('Nationality'), max_length=255, blank=True, null=True)
    age = models.CharField(_('Age'), max_length=20, blank=True, null=True)
    last_modified = models.DateTimeField(_('Last Updated'), auto_now=True)

    def __str__(self):
        return "User Profile %(user)" % {'user': self.user.get_username}
