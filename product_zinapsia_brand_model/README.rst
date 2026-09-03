===================================
Zinapsia Product Brand and Model
===================================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

This module adds a configurable Brand catalog and a free-text Model field
to products.

* **Brand** is a dedicated, configurable catalog (its own list of records,
  managed from Inventory > Configuration > Brands). It is available as a
  field on the product form, as a searchable/filterable field and as a
  "Group By" option in the product list, and as an optional column in the
  product grid.
* **Model** is a free-text field on the product form. It is available as
  an optional column in the product grid, but it is not searchable or
  usable as a "Group By" option.

The technical model and field names are namespaced under ``zinapsia`` to
avoid a naming collision with the unrelated ``product.brand`` model
shipped by other, non-Zinapsia modules.

**Table of contents**

.. contents::
   :local:

Configuration
=============

To manage the Brand catalog, go to Inventory > Configuration > Brands.
Users in the *Inventory / Administrator* group (``stock.group_stock_manager``)
can create, edit and delete brands; users in the *Inventory / User*
group (``stock.group_stock_user``) can only view them.

Usage
=====

On any product form, set the *Brand* and *Model* fields next to the
product's *Category*.

From the product list (Inventory > Products), the *Brand* field can be
used to search and filter products, to group products by brand ("Group
By" > Brand), and both *Brand* and *Model* can be enabled as optional
columns from the list's column selector.

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
