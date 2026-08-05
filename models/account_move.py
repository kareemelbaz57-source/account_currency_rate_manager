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

    @api.depends("currency_id", "currency_id.current_rate")
    def _compute_currency_rate(self):
        for move in self:
            if move.currency_id:
                move.currency_rate = move.currency_id.current_rate
            else:
                move.currency_rate = 1.0
