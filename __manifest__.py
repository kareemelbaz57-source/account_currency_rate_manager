{
    "name": "Account Currency Rate Manager",
    "version": "19.0.1.0.0",
    "summary": "Professional Currency Rate Management",
    "description": """
Professional Currency Rate Management for Odoo 19
Community & Enterprise
""",
    "category": "Accounting",
    "author": "Kareem Elbaz",
    "license": "LGPL-3",
    "depends": [
        "account",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/res_currency_views.xml",
        "views/account_move_views.xml",
        "wizard/currency_rate_update_wizard.xml",
        "data/ir_cron.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
