from datetime import timedelta
from flask import Flask, flash, render_template, request, redirect, session, url_for
from data import cars, users

app = Flask(__name__)
app.secret_key = "your_secret_key_236egsdbzdbsdghs"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=365)
app.config["SESSION_PERMANENT"] = True


@app.route("/")
def cars_list():
    if not session.get("logged_in"):
        flash("please login", "danger")
        return redirect(url_for("login"))
    # handling problem filter
    search_filter = request.args.get("search", "").lower()
    if search_filter:
        filtered_cars = []
        for car in cars:
            if search_filter in car.get("problems", []) or search_filter in car.get(
                "number"
            ):
                filtered_cars.append(car)
    else:
        filtered_cars = cars  # Return all cars if no problem filter is requested

    # handling urgent after problem filter
    urgent = request.args.get("urgent", "")
    if urgent == "true":
        new_cars = [car for car in filtered_cars if car.get("urgent")]
    else:
        new_cars = filtered_cars

    return render_template(
        "car_list.html", car_list=new_cars, search=search_filter, urgent=urgent
    )

    # speific problem filter
    # if problem_filter == "engine":
    #     filtered_cars = [car for car in cars if "engine" in car.get('problems')]

    # list comprehension is equivalent to the following code
    # new_cars = []
    # for car in cars:
    #     if car.get('urgent'):
    #         new_cars.append(car)


@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
        if car["id"] == id:
            return render_template("single_car.html", car=car)
    return render_template("single_car.html", car=None)


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if not session.get("logged_in"):
        flash("please login", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_car = {
            "id": request.form.get("id"),
            "number": request.form.get("number"),
            "urgent": request.form.get("urgent").lower()
            == "true",  # Convert to boolean
            "image": request.form.get("image"),
            "problems": [
                prob.strip()
                for prob in request.form.get("problems", "").split(",")
                if prob.strip()
            ],
        }
        cars.append(new_car)
        flash(f'Added car {new_car.get("number")}', "success")
        # return redirect('/')  # simple version of redirect
        return redirect(
            url_for("cars_list")
        )  # Redirect to cars_list route or any other page
    return render_template("add_car.html")


@app.route("/logout/")
def logout():
    session.clear()
    flash("Goodbye. please login again soon")
    return redirect(url_for("login"))


@app.route("/login/", methods=["POST", "GET"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        for user in users:
            if user.get("name") == username and user.get("password") == password:
                flash("Login successful!", "success")
                session.permanent = True
                session["logged_in"] = True
                session["username"] = username
                return redirect("/")
        flash("Error in user or password", "danger")

    return render_template("login.html")


@app.route("/delete/<id>/")
def delete(id):
    for car in cars:
        if car.get("id") == id:
            cars.remove(car)
            return redirect(url_for("cars_list"))

    return "ERROR deleting " + id


if __name__ == "__main__":
    app.run(debug=True, port=9000)
