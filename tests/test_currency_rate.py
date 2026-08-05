from odoo.tests.common import TransactionCase


class TestCurrencyRate(TransactionCase):

    def setUp(self):
        super().setUp()

        self.currency = self.env.ref("base.USD")

    def test_manual_rate_field_exists(self):
        self.assertTrue(hasattr(self.currency, "manual_rate"))

    def test_current_rate_field_exists(self):
        self.assertTrue(hasattr(self.currency, "current_rate"))

    def test_update_manual_rate_action(self):
        action = self.currency.action_update_manual_rate()

        self.assertEqual(
            action["res_model"],
            "currency.rate.update.wizard",
        )

    def test_currency_provider_exists(self):
        self.assertTrue(
            hasattr(
                self.env.company,
                "currency_provider",
            )
        )
