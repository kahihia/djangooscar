from src.base_settings import *
import dj_database_url

DEBUG = True

PAYPAL_MODE = "sandbox"  # sandbox or live
PAYPAL_CLIENT_ID = 'AVascabf623z7ZQ3td17Q19ZtrqmMm33pghypgEfZ-YouFxcRM2rbO_ED4nopU3x5kfGZJk2424z6j7o'
PAYPAL_CLIENT_SECRET = "ELk1DJS7Ohy7GUqlpGUYZCzIdgnkMWpyubU8UMHgJkkcg735NGzroUIDZgArCh4w8HIjvES4Isrsixmx"
PAYPAL_RETURN_URI = "http://127.0.0.1:8000/checkout/paypal/approve"
PAYPAL_CANCEL_URI = "http://127.0.0.1:8000/checkout/paypal/cancel"
PAYPAL_WEB_PROFILE = 'XP-UKG8-LXCW-FZD3-DCFU'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'KAMP_TEST',
#         'USER': 'kamper',
#         'PASSWORD': 'kamp12!!',
#         'HOST': '52.78.92.50',
#         'PORT': '3306',
#         'ATOMIC_REQUESTS': True,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'

    }
}


DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

