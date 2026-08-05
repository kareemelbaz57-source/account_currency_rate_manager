from odoo import api, fields, models
from ..services.frankfurter_service import FrankfurterService

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
        for currency in self:
            if currency.manual_rate <= 0:
                continue

            self.env["res.currency.rate"].create({
                "currency_id": currency.id,
                "company_id": self.env.company.id,
                "name": fields.Date.today(),
                "rate": currency.manual_rate,
            })

            currency.write({
                "last_update": fields.Datetime.now(),
                "updated_by": self.env.user.id,
            })

        return True

   def action_auto_update_rates(self):
    company = self.env.company

    base_currency = company.currency_id.name

    rates = FrankfurterService.get_rates(base_currency)

    for currency in self.search([]):

        if currency.name not in rates:
            continue

        self.env["res.currency.rate"].create({
            "currency_id": currency.id,
            "company_id": company.id,
            "name": fields.Date.today(),
            "rate": rates[currency.name],
        })

        currency.write({
            "manual_rate": rates[currency.name],
            "last_update": fields.Datetime.now(),
            "updated_by": self.env.user.id,
        })

        self.env["currency.rate.history"].create({
            "currency_id": currency.id,
            "company_id": company.id,
            "old_rate": currency.current_rate,
            "new_rate": rates[currency.name],
            "update_type": "automatic",
            "updated_by": self.env.user.id,
        })

    return True
