from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    currency_current_rate = fields.Float(
        string="Exchange Rate",
        related="currency_id.current_rate",
        digits=(12, 6),
        readonly=True,
        store=False,
    )
