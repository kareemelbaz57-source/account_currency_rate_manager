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

    @api.depends_context("company")
    def _compute_dashboard(self):
        company = self.env.company
        currency_model = self.env["res.currency"]
        history_model = self.env["currency.rate.history"]

        last_history = history_model.search(
            [("company_id", "=", company.id)],
            order="update_date desc, id desc",
            limit=1,
        )

        for record in self:
            record.currency_count = currency_model.search_count(
                [("active", "=", True)]
            )
            record.history_count = history_model.search_count(
                [("company_id", "=", company.id)]
            )
            record.last_update = (
                last_history.update_date
                or company.currency_last_sync
                or False
            )
            record.provider = dict(
                company._fields["currency_provider"].selection
            ).get(company.currency_provider, company.currency_provider)

    def action_update_now(self):
        self.ensure_one()
        self.env["res.currency"].action_auto_update_rates()

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }
