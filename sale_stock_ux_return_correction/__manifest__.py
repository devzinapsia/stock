{
    "name": "Sale Stock UX Return Correction",
    "summary": "Restores the native stock return wizard for purchase (incoming) returns",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Zinapsia",
    "website": "https://www.zinapsia.com",
    "depends": [
        "sale_stock_ux",
    ],
    "data": [
        "wizards/stock_return_picking_views.xml",
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
