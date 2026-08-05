from .frankfurter_service import FrankfurterService
from .ecb_service import ECBService


class CurrencyRateProvider:

    @staticmethod
    def get_rates(provider, base_currency):
        providers = {
            "frankfurter": FrankfurterService,
            "ecb": ECBService,
        }

        service = providers.get(provider)

        if not service:
            return {}

        return service.get_rates(base_currency)
