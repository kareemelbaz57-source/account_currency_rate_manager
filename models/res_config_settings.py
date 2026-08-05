from odoo import _, fields, models
from odoo.exceptions import UserError

from ..services.provider import CurrencyRateProvider


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    currency_rate_provider = fields.Selection(
        [
            ("manual", "Manual"),
            ("frankfurter", "Frankfurter"),
            ("ecb", "European Central Bank"),
        ],
        string="Currency Provider",
        config_parameter="account_currency_rate_manager.provider",
        default="manual",
    )

    currency_auto_update = fields.Boolean(
        string="Automatic Currency Update",
        config_parameter="account_currency_rate_manager.auto_update",
    )

    def action_test_connection(self):
        self.ensure_one()

        provider = self.currency_rate_provider

        if provider == "manual":
            raise UserError(_("Manual provider does not require testing."))

        base_currency = self.env.company.currency_id.name

        try:
            rates = CurrencyRateProvider.get_rates(
                provider,
                base_currency,
            )

            if not rates:
                raise UserError(_("No exchange rates received."))

            self.env["currency.rate.log"].create({
                "provider": provider,
                "status": "success",
                "message": "Connection successful.",
                "company_id": self.env.company.id,
            })

            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Success"),
                    "message": _("Connection successful."),
                    "sticky": False,
                },
            }

        except Exception as error:
            self.env["currency.rate.log"].create({
                "provider": provider,
                "status": "failed",
                "message": str(error),
                "company_id": self.env.company.id,
            })

            raise UserError(str(error))
