from oscar.apps.address.abstract_models import (
    AbstractCountry, AbstractUserAddress)
from oscar.core.loading import is_model_registered

__all__ = []

# user_address (회원 주소)
if not is_model_registered('address', 'UserAddress'):
    class UserAddress(AbstractUserAddress):

        pass

    __all__.append('UserAddress')

# Country (지역을 나타냄)
if not is_model_registered('address', 'Country'):
    class Country(AbstractCountry):
        pass

    __all__.append('Country')


from oscar.apps.address.models import *  # noqa
