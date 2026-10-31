====================================
Mejoras a stock y compras (Adhoc UX)
====================================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

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

**Table of contents**

.. contents::
   :local:

Configuración
=============

No requiere configuración. Alcanza con instalarlo junto con
``sale_stock_ux`` y ``purchase_stock_ux``.

**Si estaba instalado** ``sale_stock_ux_return_correction``: actualizar ese
módulo (instala este automáticamente) y después desinstalarlo.

Uso
===

**Cambio de mercadería con el proveedor**

#. Abrir la recepción de la orden de compra y hacer clic en **Devolver**.
#. Indicar los productos y cantidades y hacer clic en
   **Devolución para cambio**. No hace falta destildar nada.
#. Odoo crea la devolución y la recepción de la reposición, las dos
   vinculadas a la orden de compra.
#. Validar la devolución cuando sale la mercadería y la reposición cuando
   llega. La facturación de la orden no cambia en ningún momento.

**Devolución con nota de crédito**

#. Desde la recepción, **Devolver** → botón **Devolver**.
#. Al validar, la cantidad aparece en la columna **Devuelto** de la orden y
   queda pendiente la nota de crédito, como antes.

Las devoluciones y cambios de órdenes de venta siguen funcionando como los
define ``sale_stock_ux``.

Bug Tracker
===========

Los errores se registran en
`GitHub Issues <https://github.com/devzinapsia/stock/issues>`_.
Antes de reportar uno nuevo, revisar si ya fue informado.

Credits
=======

Authors
-------

* Zinapsia

Maintainers
-----------

Este módulo es mantenido por Zinapsia.

Este módulo es parte del proyecto
`stock <https://github.com/devzinapsia/stock>`_.
