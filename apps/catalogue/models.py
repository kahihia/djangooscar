"""
Vanilla product models
"""
import logging
import os
from datetime import date, datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.finders import find
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.base import File
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Count, Sum
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language, pgettext_lazy

from treebeard.mp_tree import MP_Node

from oscar.core.decorators import deprecated
from oscar.core.loading import get_class, get_classes, get_model
from oscar.core.utils import slugify
from oscar.core.validators import non_python_keyword
from oscar.models.fields import AutoSlugField, NullCharField
from oscar.apps.catalogue.abstract_models import *  # noqa
from oscar.core.loading import is_model_registered

__all__ = ['ProductAttributesContainer']


class Category(AbstractCategory):
    is_chinese = models.BooleanField(_('is Chinese'), default=False)
    cn_name = models.CharField(_('Cn Name'), max_length=255, db_index=True,null=True)
    cn_description = models.TextField(_('Cn Description'), blank=True,null=True)
    cn_image = models.ImageField(_('Cn_Image'), upload_to='categories', blank=True,
                                 null=True, max_length=255)

    class Meta:
        app_label = 'catalogue'
        ordering = ['path']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    #     cn용 함수 등록 필요


class ProductCategory(AbstractProductCategory):
    pass


class Product(AbstractProduct):
    is_chinese = models.BooleanField(_('is Chinese'), default=False)
    cn_title = models.CharField(pgettext_lazy(u'Product title', u'cn_Title'),
                                max_length=255, blank=True,null=True)
    cn_description = models.TextField(_('cn_Description'), blank=True,null=True)
    description_img = models.ImageField(_('Descriptionimg'), upload_to='products', blank=True,
                                 null=True, max_length=255)

#     cn용 함수 등록 필요


if not is_model_registered('catalogue', 'ProductRecommendation'):
    class ProductRecommendation(AbstractProductRecommendation):
        pass


    __all__.append('ProductRecommendation')

if not is_model_registered('catalogue', 'ProductAttribute'):
    class ProductAttribute(AbstractProductAttribute):
        pass


    __all__.append('ProductAttribute')

if not is_model_registered('catalogue', 'ProductAttributeValue'):
    class ProductAttributeValue(AbstractProductAttributeValue):
        pass


    __all__.append('ProductAttributeValue')

if not is_model_registered('catalogue', 'AttributeOptionGroup'):
    class AttributeOptionGroup(AbstractAttributeOptionGroup):
        pass


    __all__.append('AttributeOptionGroup')

if not is_model_registered('catalogue', 'AttributeOption'):
    class AttributeOption(AbstractAttributeOption):
        pass


    __all__.append('AttributeOption')

if not is_model_registered('catalogue', 'Option'):
    class Option(AbstractOption):
        pass


    __all__.append('Option')

if not is_model_registered('catalogue', 'ProductImage'):
    class ProductImage(AbstractProductImage):
        pass


    __all__.append('ProductImage')

from oscar.apps.catalogue.models import *  # noqa
