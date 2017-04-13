
from django.conf.urls import url

from . import views

urlpatterns = [
    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    url(regex="wireless/$", view=views.WirelessReservationView.as_view(), name="wireless_view"),
    url(regex="datecheck/$", view=views.DateCheckView.as_view(), name="date_check_view"),
    url(regex="delivery/$", view=views.DeliveryView.as_view(), name="delivery_view"),
]
