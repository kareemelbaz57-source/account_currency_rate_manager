from odoo.tests.common import TransactionCase


class TestCurrencyRate(TransactionCase):

    def test_create_manual_rate(self):
        currency = self.env.ref("base.USD")

        currency.manual_rate = 50

        currency.action_update_manual_rate()

        self.assertTrue(currency.current_rate > 0)
