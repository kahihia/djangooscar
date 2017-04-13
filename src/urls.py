"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from oscar.app import application

from others import urls as others_urls
from custom_categories import urls as custom_categories_urls

# from paypal.express.dashboard.app import application as CoreDashBoardApplication

# 대은 번역
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
                  url(r'i18n/', include('django.conf.urls.i18n')),
                  # The Django admin is not officially supported; expect breakage.
                  # Nonetheless, it's often useful for debugging.
                  url(r'^admin/', include(admin.site.urls)),
                  # url(r'', include(application.urls)),
                  url(r'^others/', include(others_urls, namespace="others")),
                  url(r'', include(application.urls)),
                  # 대은 : 페북 로그인 추가
                  url(r'', include('social.apps.django_app.urls', namespace='social')),
                  url(r'', include('django.contrib.auth.urls', namespace='auth')),

                  # # 윤수 : 페이팔 추가
                  # url(r'^dashboard/paypal/express/', include(CoreDashBoardApplication.urls)),
                  # # Checkout with Paypal
                  # url(r'^checkout/paypal/', include('paypal.express.urls')),
                  # url(r'^kamper_paypal/', include('kamper_paypal.urls',namespace='kamper_paypal')),
                  url(r'^', include(custom_categories_urls, namespace="custom")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # media 파일을 serve하기 위하여




# 추가 예정
urlpatterns += i18n_patterns('', url(r'', include(application.urls)),)

urlpatterns += i18n_patterns(
        url(r'', include(application.urls)),

)

