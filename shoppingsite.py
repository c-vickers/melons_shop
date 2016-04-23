"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'p1fwHB!'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<int:melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    #initiate order_total variable
    order_total = 0

    #get the cart list saved in the session. Below will get empty list if cart hasn't been created
    melons_ordered = session.get('cart', [])
    
    #initiate empty dictionary (we will add items to here later) 
    melons_dict = {}
    
    #loop over info in melons_ordered (orignally from session[cart])
    for i in melons_ordered:

        #if the item (i) is already a key in melon_dict then cart_info should equal value
        #previously added to the dictionary
        if i in melons_dict:
            cart_info = melons_dict[i]

        #if the item (i) is NOT in the dictionary...
        else:
    #Create a melon_type variable that holds info for i pulled from melons.py using method get_by_id
            melon_type = melons.get_by_id(i)
    #Assign melons_dict[i] to new variable cart_info (so it is easier to call later.)
    #The value of cart_info (a.k.a. melons_dict[i]) at i will be a nested dictionary
            cart_info = melons_dict[i] = {
    #Set the key/value pairs of the nested dictionary inside melons_dict[i] (a.k.a. cart_info) at i
    #based on info pulled into melon_type (see line85) for that i
            'common_name': melon_type.common_name,
            'unit_cost': melon_type.price,
            'qty': 0,
            'total_cost': 0,
            }
    #Call the variable cart_info (a.k.a melons_dict[i]...so a key in a dictionary)
    #Update the value of the listed nested keys
        cart_info['qty'] += 1
        cart_info['total_cost'] += cart_info['unit_cost']

        #increment order_total using unit cost
        order_total += cart_info['unit_cost']

    #unpacking your nested dictionaries by calling values
    melon_dict = melon_dict.values()

    return render_template("cart.html", cart=melon_dict, order_total=order_total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality

    # The logic here should be something like:
    #
    # - add the id of the melon they bought to the cart in the session
    if session.get('cart') != None:
        session['cart'].append(id)
    else:
        session['cart'] = [id]
    print session["cart"]
    flash("Melon added to cart!")

    return render_template("cart.html")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
