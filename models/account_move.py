from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    currency_rate = fields.Float(
        string="Exchange Rate",
        compute="_compute_currency_rate",
        digits=(12, 6),
        readonly=True,
        store=False,
    )

    @api.depends("currency_id", "company_id", "date")
    def _compute_currency_rate(self):
        CurrencyRate = self.env["res.currency.rate"]

        for move in self:
            if not move.currency_id:
                move.currency_rate = 1.0
                continue

            company = move.company_id or self.env.company
            rate_date = move.date or fields.Date.today()

            rate = CurrencyRate.search(
                [
                    ("currency_id", "=", move.currency_id.id),
                    ("name", "<=", rate_date),
                    "|",
                    ("company_id", "=", company.id),
                    ("company_id", "=", False),
                ],
                order="name desc",
                limit=1,
            )

            move.currency_rate = rate.rate if rate else 1.0
