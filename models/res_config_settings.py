from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_rate_provider = fields.Selection(
        [
            ("manual", "Manual"),
            ("frankfurter", "Frankfurter"),
        ],
        string="Currency Provider",
        config_parameter="account_currency_rate_manager.provider",
        default="manual",
    )

    currency_auto_update = fields.Boolean(
        string="Automatic Currency Update",
        config_parameter="account_currency_rate_manager.auto_update",
    )
