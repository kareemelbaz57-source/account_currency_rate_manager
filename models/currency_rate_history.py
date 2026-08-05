from odoo import fields, models


class CurrencyRateHistory(models.Model):
    _name = "currency.rate.history"
    _description = "Currency Rate History"
    _order = "update_date desc, id desc"

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        required=True,
        ondelete="cascade",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    old_rate = fields.Float(
        string="Old Rate",
        digits=(12, 6),
    )

    new_rate = fields.Float(
        string="New Rate",
        digits=(12, 6),
        required=True,
    )

    update_date = fields.Datetime(
        string="Update Date",
        default=fields.Datetime.now,
        required=True,
    )

    updated_by = fields.Many2one(
        "res.users",
        string="Updated By",
        default=lambda self: self.env.user,
        readonly=True,
    )

    update_type = fields.Selection(
        [
            ("manual", "Manual"),
            ("automatic", "Automatic"),
        ],
        string="Update Type",
        default="manual",
        required=True,
    )
