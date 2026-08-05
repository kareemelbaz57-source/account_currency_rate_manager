from odoo import api, fields, models


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

    @api.depends("rate_ids")
    def _compute_current_rate(self):
        for currency in self:
            rate = currency.rate_ids.sorted(
                key=lambda r: (r.name, r.id),
                reverse=True,
            )[:1]

            currency.current_rate = rate.rate if rate else 0.0
