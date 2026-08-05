from odoo import fields, models


class CurrencyRateUpdateWizard(models.TransientModel):
    _name = "currency.rate.update.wizard"
    _description = "Currency Rate Update Wizard"

    currency_id = fields.Many2one(
        "res.currency",
        required=True,
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    rate = fields.Float(
        string="Exchange Rate",
        digits=(12, 6),
        required=True,
    )

    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        required=True,
    )

    def action_confirm(self):
        self.ensure_one()

        old_rate = self.currency_id.current_rate

        existing_rate = self.env["res.currency.rate"].search(
            [
                ("currency_id", "=", self.currency_id.id),
                ("company_id", "=", self.company_id.id),
                ("name", "=", self.date),
            ],
            limit=1,
        )

        if existing_rate:
            existing_rate.write({
                "rate": self.rate,
            })
        else:
            self.env["res.currency.rate"].create({
                "currency_id": self.currency_id.id,
                "company_id": self.company_id.id,
                "name": self.date,
                "rate": self.rate,
            })

        self.currency_id.write({
            "manual_rate": self.rate,
            "last_update": fields.Datetime.now(),
            "updated_by": self.env.user.id,
        })

        self.env["currency.rate.history"].create({
            "currency_id": self.currency_id.id,
            "company_id": self.company_id.id,
            "old_rate": old_rate,
            "new_rate": self.rate,
            "updated_by": self.env.user.id,
            "update_type": "manual",
        })

        return {
            "type": "ir.actions.act_window_close",
        }
