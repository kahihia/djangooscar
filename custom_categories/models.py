from datetime import datetime

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.http import request
from django.utils.translation import ugettext_lazy as _

PLACE_CHOICES = (
    ('홍대', '홍대(Hongdae)'),
    ('강남', '강남(Gangnam)'),
    ('여의도', '여의도(Yeouido)'),
)


class WirelessReservation(models.Model):
    user_name = models.CharField(max_length=100, verbose_name=_("Name(passport)"))

    user = models.ForeignKey(AUTH_USER_MODEL, related_name='wireless_reservation', verbose_name=_("WirelessReserve"),
                             null=True, blank=True)

    user_email = models.EmailField(max_length=100, verbose_name=_("E-mail"))

    meet_place = models.CharField(max_length=20, choices=PLACE_CHOICES, verbose_name=_("Place"))
    meet_date = models.DateField(verbose_name=_("Date"),blank=False)

    meet_time = models.TimeField(verbose_name=_("Time"))

    recommended_user_email = models.EmailField(max_length=200, verbose_name=_("Recommended ID"), null=True, blank=True)
    recommended_user = models.ForeignKey(AUTH_USER_MODEL, related_name="recommended_wireless", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def save(self, *args, **kwargs):
        return super(WirelessReservation, self).save(*args, **kwargs)

    def __str__(self):
        return "[Wireless Reservation] user_name: %s, user_email: %s, meet_place: %s, meet_date:%s, meet_time: %s" \
               % (self.user_name, self.user_email, self.meet_place,self.meet_date, self.meet_time)
