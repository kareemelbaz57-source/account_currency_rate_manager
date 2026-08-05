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

    currency_last_sync = fields.Datetime(
        related="company_id.currency_last_sync",
        readonly=True,
    )

    def action_test_connection(self):
        self.ensure_one()

        if self.currency_provider == "manual":
            raise UserError(_("Manual provider does not require testing."))

        try:
            rates = CurrencyRateProvider.get_rates(
                self.currency_provider,
                self.company_id.currency_id.name,
            )
        except Exception as error:
            self.env["currency.rate.log"].create(
                {
                    "provider": self.currency_provider or "unknown",
                    "status": "failed",
                    "message": str(error),
                    "company_id": self.company_id.id,
                }
            )
            raise UserError(_("Connection failed: %s") % error) from error

        if not rates:
            raise UserError(_("Unable to retrieve exchange rates."))

        self.env["currency.rate.log"].create(
            {
                "provider": self.currency_provider,
                "status": "success",
                "message": _("Connection successful."),
                "company_id": self.company_id.id,
            }
        )

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Connection successful."),
                "type": "success",
                "sticky": False,
            },
        }
