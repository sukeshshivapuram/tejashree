{
    'name': 'Default Storable Products (Track Inventory by Default)',
    'version': '19.0.1.0.0',
    'summary': 'New products are Storable (Track Inventory) by default, no matter '
               'which app creates them: Sales, Purchase, Inventory or import. '
               'Users can still uncheck it manually.',
    'description': """
Default Storable Products
=========================

In Odoo 19 every new product is created as a *Good* with **Track Inventory**
(``is_storable``) **disabled**. It is very easy to forget to enable it, and a
product without inventory tracking will not appear in stock reports, valuation
or reordering.

Setting the default with *Set Defaults* (``ir.default``) does **not** solve it,
because that value is contextual and is ignored when the product is created from
Sales or Purchase.

This module overrides the default **at model level**, so every new product is
born with **Track Inventory enabled**, regardless of the app it is created from
(Sales, Purchase, Inventory, import, API...). The user can always uncheck it for
services or non-tracked goods.

Key features
------------
* New products track inventory (Storable) by default everywhere.
* Works from Sales, Purchase, Inventory, imports and the API.
* No configuration needed: install and it just works.
* Fully reversible per product with a single click.

No user data is collected or sent to any external service.
    """,
    'author': 'Intelbiz Panama',
    'website': 'https://intelbizpanama.com',
    'support': 'info@intelbizpanama.com',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
