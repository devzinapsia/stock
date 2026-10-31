=================================================
Corrección de devoluciones de compra (obsoleto)
=================================================

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

|badge1|

**Este módulo es obsoleto.** Todas sus funciones se trasladaron al módulo
``stock_ux_improvements`` (*Mejoras a stock y compras (Adhoc UX)*), que
además corrige la cantidad devuelta de las órdenes de compra después de una
devolución para cambio.

Se mantiene solo para migrar las bases donde estaba instalado.

**Table of contents**

.. contents::
   :local:

Migración
=========

En una base donde este módulo está instalado:

#. Actualizar la lista de aplicaciones.
#. **Actualizar** este módulo. Como ahora depende de ``stock_ux_improvements``,
   Odoo instala ese módulo automáticamente.
#. **Desinstalar** este módulo. No deshace nada: el asistente de devolución
   sigue funcionando igual, ahora gracias a ``stock_ux_improvements``.

En bases nuevas, instalar directamente ``stock_ux_improvements``.

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
