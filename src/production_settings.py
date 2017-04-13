from src.base_settings import *


DEBUG = False

ALLOWED_HOSTS = ["www.kamper.co.kr", "kamper.co.kr", ]



# if 'RDS_HOSTNAME' in os.environ:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.environ['RDS_DB_NAME'],
#             'USER': os.environ['RDS_USERNAME'],
#             'PASSWORD': os.environ['RDS_PASSWORD'],
#             'HOST': os.environ['RDS_HOSTNAME'],
#             'PORT': os.environ['RDS_PORT'],
#         }
#     }



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'KAMPER',
            'USER': 'kamperadmin',
            'PASSWORD': "kamp12!!",
            'HOST': "aa5ji7js1hf4fv.cqtstugh14sk.ap-northeast-2.rds.amazonaws.com",
            'PORT': '3306',
            'ATOMIC_REQUESTS': True,
        }
    }

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


PAYPAL_MODE = "live"  # sandbox or live
PAYPAL_CLIENT_ID = 'ASbP8_MmvNEjDM2-n18gsAiN838_Wwj-XRKFxe4T2n0VlXimNMzQujHrMFINp3RkrNyX3bbhRDzYLK-2'
PAYPAL_CLIENT_SECRET = "EGxchYlAC0zUY0GAaJoXqzS8yPxoT7ntCy5ZPquaO5U4Qsz27ufeE-PC4w4IoF7PGN2kt6C7QIe8mU_S"
PAYPAL_RETURN_URI = "https://kamper.co.kr/checkout/paypal/approve"
PAYPAL_CANCEL_URI = "https://kamper.co.kr/checkout/paypal/cancel"

PAYPAL_WEB_PROFILE = "XP-Y7KV-VCWP-UT8M-88JC"