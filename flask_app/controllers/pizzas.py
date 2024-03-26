from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.pizza import Pizza


@app.route("/pizzas")
def pizzas():
    if "user_id" in session:
        return render_template("pizzas.html")
    return redirect("/")


@app.route("/order")
def order():
    if "user_id" in session:
        return render_template("order.html")
    return redirect("/")


pizza_orders = []


# @app.route("/order", methods=["POST"])
# def create_pizza():
#     method = request.form.get("method")
#     crust = request.form.get("crust")
#     size = request.form.get("size")
#     quantity = request.form.get("quantity")
#     toppings = request.form.getlist("toppings")

#     # Validate the form data (you can add more validation as needed)
#     if not method or not crust or not size or not quantity or not toppings:
#         flash("Please fill out all fields.", "error")
#         return redirect("/")

#     # Save the order to the mockup database (replace with actual database interaction)
#     pizza_order = {
#         "method": method,
#         "crust": crust,
#         "size": size,
#         "quantity": quantity,
#         "toppings": toppings,
#     }
#     pizza_orders.append(pizza_order)

#     flash("Pizza order created successfully!", "success")
#     # Redirect to the validation page
#     return redirect("pizza.html")

@app.route("/pizza")
def validation_page():
    # Retrieve the last pizza order from the database using your custom method
    last_order_data = Pizza.getLastOrder()

    # Create a Pizza object from the retrieved data
    if last_order_data:
        last_order = Pizza(last_order_data)
    else:
        last_order = None

    # Pass the last pizza order to the pizza.html template
    return render_template("pizza.html", pizza=last_order)


@app.route("/order", methods=["POST"])
def createPizza():
    if "user_id" not in session:
        return redirect("/")

    # Extract pizza details from the form
    pizza_data = {
        "method": request.form["method"],
        "size": request.form["size"],
        "crust": request.form["crust"],
        "quantity": request.form["quantity"],
        "user_id": session["user_id"],
    }

    # Create the pizza and retrieve the pizza ID
    pizza_id = Pizza.create(pizza_data)

    # Extract selected toppings from the form
    # selected_toppings = request.form.getlist("topping")

    # Create records in PizzaToppings for each selected topping
    # for topping_id in selected_toppings:
    #     data_top = {"pizza_id": pizza_id, "topping_id": topping_id}
    #     Pizza.addTopping(data_top)
    #     order = {"method": pizza_data["method"],
    #          "size": pizza_data["size"],
    #          "crust": pizza_data["crust"],
    #          "quantity": pizza_data["quantity"],
    #          "toppings": selected_toppings} 

    return redirect("/pizza")




@app.route("/pizza/<int:id>")
def viewPizza(id):
    if "user_id" not in session:
        return redirect("/")
    data = {"id": id, "pizza_id": id}
    pizza = pizza.get_pizza_by_id(data)
    return redirect("/")


@app.route("/pizza/delete/<int:id>")
def deletePizza(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    pizza = Pizza.get_pizza_by_id(data)
    if pizza["user_id"] == session["user_id"]:
        Pizza.delete(data)
    return redirect("/")