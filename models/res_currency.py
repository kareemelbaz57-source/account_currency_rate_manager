from odoo import api, fields, models

from ..services.provider import CurrencyRateProvider


class ResCurrency(models.Model):
    _inherit = "res.currency"

    manual_rate = fields.Float(
        string="Manual Rate",
        digits=(12, 6),
    )

    current_rate = fields.Float(
        string="Current Rate",
        compute="_compute_current_rate",
        digits=(12, 6),
    )

    last_update = fields.Datetime(
        string="Last Update",
        readonly=True,
    )

    updated_by = fields.Many2one(
        "res.users",
        string="Updated By",
        readonly=True,
    )

    @api.depends("rate_ids.rate")
    def _compute_current_rate(self):
        for currency in self:
            rate = self.env["res.currency.rate"].search(
                [("currency_id", "=", currency.id)],
                order="name desc, id desc",
                limit=1,
            )
            currency.current_rate = rate.rate if rate else 0.0

    def action_update_manual_rate(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Update Currency Rate",
            "res_model": "currency.rate.update.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_currency_id": self.id,
                "default_company_id": self.env.company.id,
                "default_rate": self.current_rate or 1.0,
            },
        }

    def action_auto_update_rates(self):
        company = self.env.company
        provider = company.currency_provider

        if provider == "manual":
            return True

        base_currency = company.currency_id.name

        rates = CurrencyRateProvider.get_rates(
            provider,
            base_currency,
        )

        if not rates:
            return True

        today = fields.Date.today()

        for currency in self.search([]):
            new_rate = rates.get(currency.name)

            if not new_rate:
                continue

            old_rate = currency.current_rate

            rate_record = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", currency.id),
                    ("company_id", "=", company.id),
                    ("name", "=", today),
                ],
                limit=1,
            )

            if rate_record:
                rate_record.write({
                    "rate": new_rate,
                })
            else:
                self.env["res.currency.rate"].create({
                    "currency_id": currency.id,
                    "company_id": company.id,
                    "name": today,
                    "rate": new_rate,
                })

            currency.write({
                "manual_rate": new_rate,
                "last_update": fields.Datetime.now(),
                "updated_by": self.env.user.id,
            })

            self.env["currency.rate.history"].create({
                "currency_id": currency.id,
                "company_id": company.id,
                "old_rate": old_rate,
                "new_rate": new_rate,
                "update_type": "automatic",
                "updated_by": self.env.user.id,
            })

        return True
