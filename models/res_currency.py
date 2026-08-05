from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..services.provider import CurrencyRateProvider


class ResCurrency(models.Model):
    _inherit = "res.currency"

    manual_rate = fields.Float(
        string="Manual Rate",
        digits=(12, 6),
        default=1.0,
    )

    current_rate = fields.Float(
        string="Current Rate",
        compute="_compute_current_rate",
        digits=(12, 6),
        readonly=True,
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

    @api.depends_context("company")
    def _compute_current_rate(self):
        company = self.env.company
        rate_date = fields.Date.context_today(self)

        for currency in self:
            if currency == company.currency_id:
                currency.current_rate = 1.0
                continue

            rate_record = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", currency.id),
                    ("name", "<=", rate_date),
                    "|",
                    ("company_id", "=", company.id),
                    ("company_id", "=", False),
                ],
                order="company_id desc, name desc, id desc",
                limit=1,
            )

            currency.current_rate = rate_record.rate if rate_record else 0.0

    def action_update_manual_rate(self):
        for currency in self:
            if currency.manual_rate <= 0:
                raise UserError(_("The exchange rate must be greater than zero."))

            company = self.env.company
            today = fields.Date.context_today(currency)

            existing_rate = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", currency.id),
                    ("company_id", "=", company.id),
                    ("name", "=", today),
                ],
                limit=1,
            )

            old_rate = existing_rate.rate if existing_rate else currency.current_rate

            values = {
                "currency_id": currency.id,
                "company_id": company.id,
                "name": today,
                "rate": currency.manual_rate,
            }

            if existing_rate:
                existing_rate.write({"rate": currency.manual_rate})
            else:
                self.env["res.currency.rate"].create(values)

            currency.write(
                {
                    "last_update": fields.Datetime.now(),
                    "updated_by": self.env.user.id,
                }
            )

            self.env["currency.rate.history"].create(
                {
                    "currency_id": currency.id,
                    "company_id": company.id,
                    "old_rate": old_rate,
                    "new_rate": currency.manual_rate,
                    "updated_by": self.env.user.id,
                    "update_type": "manual",
                }
            )

        return True

    @api.model
    def action_auto_update_rates(self):
        companies = self.env["res.company"].search(
            [
                ("currency_auto_update", "=", True),
            ]
        )

        for company in companies:
            provider = company.currency_provider

            if not provider or provider == "manual":
                continue

            try:
                rates = CurrencyRateProvider.get_rates(
                    provider,
                    company.currency_id.name,
                )

                if not rates:
                    self.env["currency.rate.log"].create(
                        {
                            "provider": provider,
                            "status": "failed",
                            "message": _("No exchange rates were returned."),
                            "company_id": company.id,
                        }
                    )
                    continue

                today = fields.Date.context_today(self)
                currencies = self.search([("active", "=", True)])

                for currency in currencies:
                    if currency == company.currency_id:
                        continue

                    rate = rates.get(currency.name)

                    if not rate or rate <= 0:
                        continue

                    existing_rate = self.env["res.currency.rate"].search(
                        [
                            ("currency_id", "=", currency.id),
                            ("company_id", "=", company.id),
                            ("name", "=", today),
                        ],
                        limit=1,
                    )

                    old_rate = existing_rate.rate if existing_rate else 0.0

                    if existing_rate:
                        existing_rate.write({"rate": rate})
                    else:
                        self.env["res.currency.rate"].create(
                            {
                                "currency_id": currency.id,
                                "company_id": company.id,
                                "name": today,
                                "rate": rate,
                            }
                        )

                    currency.write(
                        {
                            "manual_rate": rate,
                            "last_update": fields.Datetime.now(),
                            "updated_by": self.env.user.id,
                        }
                    )

                    self.env["currency.rate.history"].create(
                        {
                            "currency_id": currency.id,
                            "company_id": company.id,
                            "old_rate": old_rate,
                            "new_rate": rate,
                            "updated_by": self.env.user.id,
                            "update_type": "automatic",
                        }
                    )

                company.currency_last_sync = fields.Datetime.now()

                self.env["currency.rate.log"].create(
                    {
                        "provider": provider,
                        "status": "success",
                        "message": _("Currency rates updated successfully."),
                        "company_id": company.id,
                    }
                )

            except Exception as error:
                self.env["currency.rate.log"].create(
                    {
                        "provider": provider or "unknown",
                        "status": "failed",
                        "message": str(error),
                        "company_id": company.id,
                    }
                )

        return True
