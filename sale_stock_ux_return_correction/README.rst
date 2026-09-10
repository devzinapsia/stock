=================================
Sale Stock UX Return Correction
=================================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

**Why this module exists**

``sale_stock_ux`` (ADHOC) adds a "Para Abonar (actualizar OC/OV)" column
and an explanatory banner to Odoo's native stock return wizard, and it
also blocks Odoo's native "Devolución para cambio" (Create exchanges)
button whenever any return line is marked ``to_refund``, raising:

    You cannot create exchanges for return lines marked to refund.

That column is really Odoo's own native ``to_refund`` field (added by
core ``stock_account``, normally hidden behind Developer Mode). On
purchase orders it defaults to ``True`` on every line, so in practice
this error fires on **every** purchase return where you want to use
"Devolución para cambio" to ask a vendor to resend defective goods,
forcing the user to manually untick "Para Abonar" first every time.

We traced why ``sale_stock_ux`` enforces this: it tags the resulting
exchange move with its own ``is_exchange_move`` flag, which
``sale.order.line`` uses to keep ``qty_delivered`` accurate for **sale**
exchanges (``models/sale_order_line.py``). That flag has no consumer
anywhere on the purchase side (checked across every ``ingadhoc/purchase``
and ``ingadhoc/stock`` module in this client's deployment) — so for
purchase returns, the restriction protects nothing and only gets in the
way.

**What this module does**

* Deactivates ``sale_stock_ux``'s inherited view on the return wizard
  (its banner and the "Para Abonar (actualizar OC/OV)" column), so the
  wizard falls back to plain native Odoo: ``to_refund`` stays hidden
  behind Developer Mode + the list's column selector, as in stock Odoo.
* On **purchase (incoming)** returns only, ``action_create_exchanges``
  calls Odoo's native implementation directly, skipping
  ``sale_stock_ux``'s check entirely.
* **Sale (outgoing)** returns and exchanges are left completely
  untouched — they keep going through ``sale_stock_ux`` exactly as
  before, so ``qty_delivered`` stays correct there.
* An uninstall hook restores ``sale_stock_ux``'s view to active again
  when this module is removed, since Odoo's automatic uninstall cleanup
  only reverts records a module *created*, not ones it only modified
  (deactivating an existing record doesn't get undone automatically).

**Table of contents**

.. contents::
   :local:

Configuration
=============

No configuration is needed. Installing this module alongside
``sale_stock_ux`` is enough to restore the native behavior described
below.

Usage
=====

On a purchase order's receipt, open the return wizard (*Devolver*) and
click *Devolución para cambio* (*Create exchanges*): it will run without
the "You cannot create exchanges for return lines marked to refund"
error, and without needing to manually untick "Para Abonar" first.

Sale order returns and exchanges keep working exactly as ``sale_stock_ux``
defines them, unchanged.

Uninstalling this module automatically restores ``sale_stock_ux``'s own
view (banner + "Para Abonar" column) on the return wizard.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/devzinapsia/stock/issues>`_.

Credits
=======

Authors
-------

* Zinapsia

Maintainers
-----------

This module is maintained by Zinapsia.
