from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    currency_rate = fields.Float(
        string="Exchange Rate",
        compute="_compute_currency_rate",
        digits=(12, 6),
        readonly=True,
    )

    @api.depends("currency_id")
    def _compute_currency_rate(self):
        for move in self:
            if not move.currency_id:
                move.currency_rate = 1.0
                continue

            company = move.company_id or self.env.company

            rate = self.env["res.currency.rate"].search(
                [
                    ("currency_id", "=", move.currency_id.id),
                    "|",
                    ("company_id", "=", company.id),
                    ("company_id", "=", False),
                ],
                order="name desc",
                limit=1,
            )

            move.currency_rate = rate.rate if rate else 1.0
