"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 1.8.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# oscar import
import paypalrestsdk
from oscar.defaults import *

# TEMPLATE import
from oscar import OSCAR_MAIN_TEMPLATE_DIR, get_core_apps

# 대은 번역
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-h=g=i%a93v)8q0*-h5l1%8n$hyd%^hu%b6e#p_tpd95vedjv@'

# SECURITY WARNING: don't run with debug turned on in production!


INSTALLED_APPS = [
                     'django.contrib.admin',
                     'django.contrib.auth',
                     'django.contrib.contenttypes',
                     'django.contrib.sessions',
                     'django.contrib.messages',
                     'django.contrib.staticfiles',
                     # 추가
                     'django.contrib.sites',
                     'django.contrib.flatpages',

                     'compressor',
                     'widget_tweaks',
                     'django_mobile',

                     # 대은 페북 로그
                     'social.apps.django_app.default',
                     # 'paypal',
                     'currency',
                     'storages',
                     'custom_categories',
                     # 'temp_paypal',
                 ] + get_core_apps(
        [
            'apps.address',
            'apps.analytics',
            'apps.basket',
            'apps.catalogue',
            'apps.checkout',
            'apps.customer',
            'apps.dashboard',
            'apps.offer',
            'apps.order',
            'apps.partner',
            'apps.payment',
            # 'apps.promotions',
            'apps.shipping',
            'apps.voucher',
            'apps.wishlists',
            'apps.dashboard.catalogue',
        ]
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 대은 번역 추가
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 추가
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'oscar.apps.basket.middleware.BasketMiddleware',
    # 추가 예정
    # 'django.middleware.locale.LocaleMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

)

ROOT_URLCONF = 'src.urls'

# AUTHENTICATION 추가
AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',

    # 대은 페북 로그인
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
           # os.path.join(BASE_DIR, 'templates/kamper'),
            # OSCAR_MAIN_TEMPLATE_DIR,
             os.path.join(BASE_DIR, 'templates/oscar'),
        ]
        ,
        # 'APP_DIRS': True,
        'OPTIONS': dict(context_processors=[
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            # media 파일을 위한 context_processor
            'django.template.context_processors.media',

            # oscar options context_processors import
            'oscar.apps.search.context_processors.search_form',
            'oscar.apps.promotions.context_processors.promotions',
            'oscar.apps.checkout.context_processors.checkout',
            'oscar.apps.customer.notifications.context_processors.notifications',
            'oscar.core.context_processors.metadata',

            # 대은 번역 추가
            'django.template.context_processors.i18n',

            # 대은 페북 로그인
            'social.apps.django_app.context_processors.backends',
            'social.apps.django_app.context_processors.login_redirect',
            'django_mobile.context_processors.flavour',
            "django_mobile.context_processors.is_mobile",

            'django.core.context_processors.request',
        ], loaders=[
            'django_mobile.loader.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    },
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

WSGI_APPLICATION = 'src.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGES = (
    ('en', _('English')),
    ('zh-cn', _('Chinese')),
)
LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'Asia/Seoul'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_URL = '/media/'

# For oscar

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

OSCAR_SHOP_NAME = 'KAMPER'

# VERSION Checking
# DISPLAY_VERSION = True
VERSION = '0.0.1'

# Django SMTP (EMAIL)
EMAIL_HOST = 'smtp.worksmobile.com'
# EMAIL_PORT = 25  # Default설정
EMAIL_HOST_USER = 'admin@kamper.co.kr'
EMAIL_HOST_PASSWORD = 'us621011'
EMAIL_PORT = 465
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True

# 대은 페북 로그
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
# 대은 : 페북 로그인 추가
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '585610984955777'
SOCIAL_AUTH_FACEBOOK_SECRET = '73edcfb69b45cda09016ac61c576737a'

# 대은 : 페북 로그인 추가
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'picture']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email,id,name,first_name,last_name,age_range,link,gender,locale,picture,timezone,updated_time,verified'
}

# 익명 구입 가능 여부
OSCAR_ALLOW_ANON_CHECKOUT = False

OSCAR_INITIAL_ORDER_STATUS = 'Order Completed'
OSCAR_ORDER_STATUS_PIPELINE = {
    'Order Completed': ('Paid', 'Order Cancelled',),  # 주문 완료
    'OrderCancelled': (),  # 입금 전 취소

    'Paid': ('Before Shipping', 'Cancel Payment',),  # 결제 완료
    'Cancel Payment': ('Cancel Payment Success'),  # 결제 취소
    'Cancel Payment Success': (),  # 결제 취소 성공

    'Before Shipping': ('Shipping-OnTheWay', 'Cancel Payment',),  # 배송 전
    'Shipping-OnTheWay': ('Shipping Completed',),  # 배송 중
    'Shipping Completed': ('FINISH',),  # 배송 완료

    'FINISH': ('Request Refund', 'Cancelled',),
    # 반품
    'Request Refund': ('Refund Cancel', 'Refund-OnTheWay',),  # 반품 신청
    'Refund Cancel': ('FINISH',),  # 반품 신청 취소

    'Refund-OnTheWay': ('Refund Received',),  # 반품 배송중
    'Refund Received': ('Refund Error', 'Refund Complete',),  # 반품 물품 수령
    'Refund Error': (),  # 반품 물건 이상
    'Refund Complete': (),  # 반품 완료
}

OSCAR_INITIAL_LINE_STATUS = 'Order Completed'
OSCAR_LINE_STATUS_PIPELINE = {
    'Order Completed': ('Paid', 'Order Cancelled',),  # 주문 완료
    'OrderCancelled': (),  # 입금 전 취소

    'Paid': ('Before Shipping', 'Cancel Payment',),  # 결제 완료
    'Cancel Payment': ('Cancel Payment Success'),  # 결제 취소
    'Cancel Payment Success': (),  # 결제 취소 성공

    'Before Shipping': ('Shipping-OnTheWay', 'Cancel Payment',),  # 배송 전
    'Shipping-OnTheWay': ('Shipping Completed',),  # 배송 중
    'Shipping Completed': ('FINISH',),  # 배송 완료

    'FINISH': ('Request Refund', 'Cancelled',),
    # 반품
    'Request Refund': ('Refund Cancel', 'Refund-OnTheWay',),  # 반품 신청
    'Refund Cancel': ('FINISH',),  # 반품 신청 취소

    'Refund-OnTheWay': ('Refund Received',),  # 반품 배송중
    'Refund Received': ('Refund Error', 'Refund Complete',),  # 반품 물품 수령
    'Refund Error': (),  # 반품 물건 이상
    'Refund Complete': (),  # 반품 완료
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

THUMBNAIL_FORCE_OVERWRITE = True

CURRENCY_KRW_PER_RMB = 160
CURRENCY_KRW_PER_USD = 1100

PAYPAL_CURRENCY = "USD"



DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAIZCHWORY5623U4RQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'elasticbeanstalk-mediafiles'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

OSCAR_DEFAULT_CURRENCY = 'KRW'

# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)


MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

AWS_S3_HOST = 's3.ap-northeast-2.amazonaws.com'

#
# OSCAR_DASHBOARD_NAVIGATION += [
#     {
#         'label': _('Wireless'),
#         'icon': 'icon-bar-chart',
#         'url_name': 'dashboard:check_wireless_view',
#     },
# ]
