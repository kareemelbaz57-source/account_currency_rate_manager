from odoo.tests.common import TransactionCase


class TestCurrencyWizard(TransactionCase):

    def test_wizard(self):

        usd = self.env.ref("base.USD")

        wizard = self.env["currency.rate.update.wizard"].create({
            "currency_id": usd.id,
            "company_id": self.env.company.id,
            "rate": 50,
        })

        wizard.action_confirm()

        self.assertEqual(usd.manual_rate, 50)
