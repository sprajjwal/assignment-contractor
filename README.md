# Welcome to your Store

A basic store website made with Flask, Jinja and MongoDB withe CRUD on items with a searchbar that let's you search off keywords instead of fully matching names.
example, searching for apple will return all items with Apple in the names similarly searching for 10 will show all items with the 10 in their names.

Items:
This store website lets you add/edit/delete new items. The items are always displayed alphabetically making it so items from sam brand would always show up next to each other.

Item fields:
    1. Name: this is supposed to be used by the item creator to add tags/queries users might use to search up the item (always, lower case).
    2. Display Name: this is the exact name the user might see(Case sensitive).
    3. Price: How much the product costs
    4. In stock: How many of the item is available in stock
    5. Images: links/url to images for the item.


