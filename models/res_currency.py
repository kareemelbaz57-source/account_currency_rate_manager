from odoo import api, fields, models

from ..services.provider import CurrencyRateProvider


class ResCurrency(models.Model):
    _inherit = "res.currency"

def action_auto_update_rates(self):
    companies = self.env["res.company"].search([
        ("currency_auto_update", "=", True),
    ])

    for company in companies:

        provider = company.currency_provider

        if provider == "manual":
            continue

        rates = CurrencyRateProvider.get_rates(
            provider,
            company.currency_id.name,
        )

        if not rates:
            continue

        today = fields.Date.today()

        currencies = self.search([])

        for currency in currencies:

            rate = rates.get(currency.name)

            if not rate:
                continue

            existing = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", currency.id),
                    ("company_id", "=", company.id),
                    ("name", "=", today),
                ],
                limit=1,
            )

            if existing:
                existing.write({
                    "rate": rate,
                })
            else:
                self.env["res.currency.rate"].create({
                    "currency_id": currency.id,
                    "company_id": company.id,
                    "name": today,
                    "rate": rate,
                })

            currency.write({
                "manual_rate": rate,
                "last_update": fields.Datetime.now(),
                "updated_by": self.env.user.id,
            })

        company.currency_last_sync = fields.Datetime.now()

    return True
