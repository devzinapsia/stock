{
    "name": "Zinapsia Product Brand and Model",
    "summary": "Adds a configurable Brand catalog and a free-text Model field to products",
    "version": "19.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "Zinapsia",
    "website": "https://www.zinapsia.com",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/zinapsia_product_brand_views.xml",
        "views/product_template_views.xml",
    ],
    "auto_install": True,
    "application": False,
    "installable": True,
}
