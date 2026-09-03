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
