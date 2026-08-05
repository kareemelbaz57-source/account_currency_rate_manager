from .frankfurter_service import FrankfurterService
from .ecb_service import ECBService


class CurrencyRateProvider:

    @staticmethod
    def get_rates(provider, base_currency):
        if provider == "frankfurter":
            return FrankfurterService.get_rates(base_currency)

        if provider == "ecb":
            return ECBService.get_rates(base_currency)

        return {}
