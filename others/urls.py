
from django.conf.urls import url

from . import views

urlpatterns = [
    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.
    url(regex="aboutus/$", view=views.AboutView.as_view(), name="aboutusView"),
    url(regex="members/$", view=views.MemberView.as_view(), name="memberView"),
    url(regex="useragreement/$", view=views.UseragreementView.as_view(), name="useragreementView"),
    url(regex="privacypolicy/$", view=views.PrivacypolicyView.as_view(), name="privacypolicyView"),
    url(regex="contactus/$", view=views.ContactusView.as_view(), name="contactusView"),
    url(regex="privacypolicyKR/$", view=views.PrivacypolicyKRView.as_view(), name="privacypolicyKRView"),
    url(regex="useragreementKR/$", view=views.UseragreementKRView.as_view(), name="useragreementKRView"),


    # url(regex="obroute/(?P<pk>\d+)/$", view= views.OrderRouteView.as_view(permanent=True), name="orderRouteView"),

]
