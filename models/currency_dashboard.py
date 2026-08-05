from odoo import api, fields, models


class CurrencyDashboard(models.TransientModel):
    _name = "currency.dashboard"
    _description = "Currency Dashboard"

    currency_count = fields.Integer(
        string="Currencies",
        compute="_compute_dashboard",
    )

    history_count = fields.Integer(
        string="History Records",
        compute="_compute_dashboard",
    )

    last_update = fields.Datetime(
        string="Last Update",
        compute="_compute_dashboard",
    )

    provider = fields.Char(
        string="Provider",
        compute="_compute_dashboard",
    )

    @api.depends()
    def _compute_dashboard(self):
        currency_model = self.env["res.currency"]
        history_model = self.env["currency.rate.history"]

        last_currency = currency_model.search(
            [],
            order="last_update desc",
            limit=1,
        )

        for record in self:
            record.currency_count = currency_model.search_count([])
            record.history_count = history_model.search_count([])
            record.last_update = last_currency.last_update
            record.provider = self.env.company.currency_provider

    def action_update_now(self):
        self.env["res.currency"].action_auto_update_rates()

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
