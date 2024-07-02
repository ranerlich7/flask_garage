from flask import Flask, render_template

app = Flask(__name__)

car1 = {
    "id": "1",
    "number": "123-456",
    "problems": [],
    "image": "https://images.pexels.com/photos/1592384/pexels-photo-1592384.jpeg?auto=compress&cs=tinysrgb&w=600",
}
car2 = {
    "id": "2",
    "number": "456-789",
    "problems": [],
    "image": "https://images.pexels.com/photos/112460/pexels-photo-112460.jpeg?auto=compress&cs=tinysrgb&w=600",
}
cars = [car1, car2]


@app.route("/")
def cars_list():
    return render_template("car_list.html", car_list=cars)

    # final_str = ""
    # for car in cars:
    #     final_str += f"<p>{car['number']}</p>"

    # return final_str


@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
        if car["id"] == id:
            return render_template("single_car.html", car=car)
    return render_template("single_car.html", car=None)


@app.route("/add_car/")
def add_car():
    print("****** Adding car")
    return "Adding car"


if __name__ == "__main__":
    app.run(debug=True, port=9000)
