# custom_storages.py
import os

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

os.environ['S3_USE_SIGV4'] = 'True'

# class StaticStorage(S3BotoStorage):
#
#     @property
#     def connection(self):
#         if self._connection is None:
#             self._connection = self.connection_class(
#                     self.access_key, self.secret_key,
#                     calling_format=self.calling_format, host='s3.eu-central-1.amazonaws.com')
#         return self._connection
#
#     location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connection_class(
                    self.access_key, self.secret_key,
                    calling_format=self.calling_format, host='s3.ap-northeast-2.amazonaws.com')
        return self._connection
    location = settings.MEDIAFILES_LOCATION
