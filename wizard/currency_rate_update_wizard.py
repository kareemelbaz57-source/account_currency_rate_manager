from odoo import fields, models


class CurrencyRateUpdateWizard(models.TransientModel):
    _name = "currency.rate.update.wizard"
    _description = "Currency Rate Update Wizard"

    currency_id = fields.Many2one(
        "res.currency",
        required=True,
    )

    rate = fields.Float(
        string="Exchange Rate",
        required=True,
        digits=(12, 6),
    )

    def action_confirm(self):
        self.env["res.currency.rate"].create({
            "currency_id": self.currency_id.id,
            "company_id": self.env.company.id,
            "name": fields.Date.today(),
            "rate": self.rate,
        })

        self.currency_id.write({
            "last_update": fields.Datetime.now(),
            "updated_by": self.env.user.id,
        })

        return {"type": "ir.actions.act_window_close"}
