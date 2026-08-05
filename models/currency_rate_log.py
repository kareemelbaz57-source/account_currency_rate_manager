from odoo import fields, models


class CurrencyRateLog(models.Model):
    _name = "currency.rate.log"
    _description = "Currency Rate Log"
    _order = "create_date desc"

    create_date = fields.Datetime(
        string="Date",
        readonly=True,
    )

    provider = fields.Char(
        string="Provider",
        required=True,
    )

    status = fields.Selection(
        [
            ("success", "Success"),
            ("failed", "Failed"),
        ],
        required=True,
    )

    message = fields.Text(
        string="Message",
    )

    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
