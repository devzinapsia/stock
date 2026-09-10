On a purchase order's receipt, open the return wizard (*Devolver*) and
click *Devolución para cambio* (*Create exchanges*): it will run without
the "You cannot create exchanges for return lines marked to refund"
error, and without needing to manually untick "Para Abonar" first.

Sale order returns and exchanges keep working exactly as ``sale_stock_ux``
defines them, unchanged.

Uninstalling this module automatically restores ``sale_stock_ux``'s own
view (banner + "Para Abonar" column) on the return wizard.
