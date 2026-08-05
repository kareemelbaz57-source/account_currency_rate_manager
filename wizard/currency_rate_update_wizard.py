from odoo import api, fields, models


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
        default=fields.Date.context_today,
        required=True,
    )

    def action_confirm(self):
    self.ensure_one()

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

    return {"type": "ir.actions.act_window_close"}
        self.env["res.currency.rate"].create({
            "currency_id": self.currency_id.id,
            "company_id": self.company_id.id,
            "name": self.date,
            "rate": self.rate,
        })

        self.currency_id.write({
            "last_update": fields.Datetime.now(),
            "updated_by": self.env.user.id,
        })

        return {"type": "ir.actions.act_window_close"}
