Reúne las mejoras de Zinapsia sobre los módulos ``sale_stock_ux`` y
``purchase_stock_ux`` de ADHOC. Reemplaza al módulo
``sale_stock_ux_return_correction``.

**1. Devoluciones de compra con cambio (asistente de devolución nativo)**

``sale_stock_ux`` agrega al asistente de devolución una columna
"Para Abonar (actualizar OC/OV)" con un banner explicativo, y bloquea el
botón nativo **Devolución para cambio** cuando alguna línea está marcada para
abonar, con el error:

    You cannot create exchanges for return lines marked to refund.

Esa columna es el campo nativo ``to_refund`` de Odoo, que en compras viene
siempre marcado, así que el error aparecía en **todas** las devoluciones de
compra para cambio. La restricción solo tiene sentido en ventas, donde
``sale_stock_ux`` la usa para mantener correcta la cantidad entregada.

Este módulo:

* Desactiva la vista de ``sale_stock_ux`` sobre el asistente (banner y
  columna "Para Abonar"). El asistente vuelve a ser el nativo de Odoo: el
  campo queda oculto como columna opcional y sigue viniendo marcado.
* En devoluciones **de compra** (recepciones), **Devolución para cambio**
  ejecuta directamente la acción nativa de Odoo, sin el bloqueo.
* Las devoluciones y cambios **de venta** siguen pasando por
  ``sale_stock_ux`` sin cambios.
* Al desinstalarlo, vuelve a activar la vista de ``sale_stock_ux``.

**2. Cantidad devuelta correcta después de un cambio (órdenes de compra)**

``purchase_stock_ux`` agrega en las líneas de compra la columna **Devuelto**
y, en los productos que se facturan **sobre cantidades ordenadas**, descuenta
lo devuelto de lo que queda por facturar. Pero también contaba como devuelto
lo que salió en una **devolución para cambio**, aunque el proveedor después lo
repone. Resultado: la orden quedaba para siempre en *Facturas en espera* con
una cantidad negativa, y **Crear Factura** generaba una nota de crédito que
no correspondía.

Este módulo deja de contar como devueltas las devoluciones que tienen una
reposición (cambio) vigente:

* Mientras la reposición está pendiente, la orden muestra la recepción como
  parcial y la facturación no cambia.
* Al recibir la reposición, la orden vuelve a quedar recibida por completo.
* Si la reposición se cancela, la devolución vuelve a contar como devuelta
  (y, por lo tanto, como pendiente de nota de crédito).
* Las devoluciones comunes (botón **Devolver**) siguen contando igual que
  antes.
