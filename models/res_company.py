from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    currency_provider = fields.Selection(
        [
            ("manual", "Manual"),
            ("frankfurter", "Frankfurter"),
            ("ecb", "European Central Bank"),
        ],
        string="Currency Provider",
        default="manual",
    )

    currency_auto_update = fields.Boolean(
        string="Automatic Currency Update",
        default=False,
    )

    currency_update_interval = fields.Integer(
        string="Update Interval (Hours)",
        default=24,
    )

    currency_last_sync = fields.Datetime(
        string="Last Synchronization",
        readonly=True,
    )
