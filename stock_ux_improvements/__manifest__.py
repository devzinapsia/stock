{
    "name": "Mejoras a stock y compras (Adhoc UX)",
    "summary": "Devoluciones de compra con cambio nativas y cantidades devueltas correctas tras un cambio",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Zinapsia",
    "website": "https://www.zinapsia.com",
    "depends": [
        "sale_stock_ux",
        "purchase_stock_ux",
    ],
    "data": [
        "wizards/stock_return_picking_views.xml",
    ],
    "auto_install": False,
    "application": False,
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
