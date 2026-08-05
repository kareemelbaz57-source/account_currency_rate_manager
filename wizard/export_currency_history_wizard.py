from io import BytesIO
import base64

from openpyxl import Workbook

from odoo import fields, models


class ExportCurrencyHistoryWizard(models.TransientModel):
    _name = "export.currency.history.wizard"
    _description = "Export Currency History"

    file_data = fields.Binary(
        readonly=True,
    )

    file_name = fields.Char(
        readonly=True,
    )

    def action_export(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Currency History"

        sheet.append([
            "Date",
            "Currency",
            "Company",
            "Old Rate",
            "New Rate",
            "Type",
            "Updated By",
        ])

        records = self.env["currency.rate.history"].search(
            [],
            order="update_date desc",
        )

        for record in records:
            sheet.append([
                str(record.update_date),
                record.currency_id.name,
                record.company_id.name,
                record.old_rate,
                record.new_rate,
                record.update_type,
                record.updated_by.name,
            ])

        output = BytesIO()
        workbook.save(output)

        self.file_data = base64.b64encode(output.getvalue())
        self.file_name = "currency_history.xlsx"

        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
