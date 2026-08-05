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

    @api.depends("rate_ids.rate")
    def _compute_current_rate(self):
        for currency in self:
            rate = self.env["res.currency.rate"].search(
                [("currency_id", "=", currency.id)],
                order="name desc,id desc",
                limit=1,
            )

            currency.current_rate = rate.rate if rate else 0.0

    def action_update_manual_rate(self):
        for currency in self:
            if currency.manual_rate <= 0:
                continue

            self.env["res.currency.rate"].create({
                "currency_id": currency.id,
                "company_id": self.env.company.id,
                "name": fields.Date.today(),
                "rate": currency.manual_rate,
            })

            currency.last_update = fields.Datetime.now()
            currency.updated_by = self.env.user
