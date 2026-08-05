from odoo import _, fields, models
from odoo.exceptions import UserError

from ..services.provider import CurrencyRateProvider


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_provider = fields.Selection(
        related="company_id.currency_provider",
        readonly=False,
    )

    currency_auto_update = fields.Boolean(
        related="company_id.currency_auto_update",
        readonly=False,
    )

    currency_update_interval = fields.Integer(
        related="company_id.currency_update_interval",
        readonly=False,
    )

    def action_test_connection(self):
        self.ensure_one()

        if self.currency_provider == "manual":
            raise UserError(_("Manual provider does not require testing."))

        rates = CurrencyRateProvider.get_rates(
            self.currency_provider,
            self.company_id.currency_id.name,
        )

        if not rates:
            raise UserError(_("Connection failed."))

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Connection successful."),
                "sticky": False,
            },
        }
