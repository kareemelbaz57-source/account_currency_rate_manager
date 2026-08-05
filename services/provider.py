from .frankfurter_service import FrankfurterService
from .ecb_service import ECBService


class CurrencyRateProvider:

    PROVIDERS = {
        "frankfurter": FrankfurterService,
        "ecb": ECBService,
    }

    @classmethod
    def get_rates(cls, provider, base_currency):
        service = cls.PROVIDERS.get(provider)

        if not service:
            return {}

        return service.get_rates(base_currency)
