# Transitional module: all its features moved to stock_ux_improvements,
# which is now its only dependency. Upgrading this module installs
# stock_ux_improvements; uninstalling it afterwards leaves everything in
# place (there is no uninstall hook anymore, so sale_stock_ux's return
# wizard view stays deactivated by stock_ux_improvements).
