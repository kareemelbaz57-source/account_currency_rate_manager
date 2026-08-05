import requests


class ECBService:
    """
    Temporary implementation.
    TODO: Replace with the official ECB API.
    """

    BASE_URL = "https://api.frankfurter.app/latest"

    @classmethod
    def get_rates(cls, base_currency):
        try:
            response = requests.get(
                cls.BASE_URL,
                params={"from": base_currency},
                timeout=20,
            )

            response.raise_for_status()

            return response.json().get("rates", {})

        except requests.RequestException:
            return {}
