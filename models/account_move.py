from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    currency_rate = fields.Float(
        string="Exchange Rate",
        compute="_compute_currency_rate",
        digits=(12, 6),
        readonly=True,
    )

    @api.depends("currency_id", "company_id", "date", "invoice_date")
    def _compute_currency_rate(self):
        for move in self:
            company = move.company_id or self.env.company
            currency = move.currency_id or company.currency_id
            rate_date = move.invoice_date or move.date or fields.Date.context_today(move)

            if currency == company.currency_id:
                move.currency_rate = 1.0
                continue

            move.currency_rate = currency._get_conversion_rate(
                from_currency=currency,
                to_currency=company.currency_id,
                company=company,
                date=rate_date,
            )
