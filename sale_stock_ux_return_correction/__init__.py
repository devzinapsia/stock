from . import wizards


def uninstall_hook(env):
    # Restore sale_stock_ux's own return wizard view: we only deactivated
    # it (wizards/stock_return_picking_views.xml), we never created it, so
    # Odoo's regular uninstall cleanup won't touch it on its own.
    adhoc_view = env.ref("sale_stock_ux.view_stock_return_picking_form", raise_if_not_found=False)
    if adhoc_view:
        adhoc_view.active = True
