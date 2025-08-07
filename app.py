from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = os.urandom(15)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


class Prod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(20), nullable=False, unique=True)
    producer = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    width = db.Column(db.String(20), nullable=False)
    depth = db.Column(db.String(20), nullable=False)
    height = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.String(20), nullable=False)
    volume = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    colling = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    energy_efficiency = db.Column(db.String(20), nullable=False)
    compressors = db.Column(db.String(20), nullable=False)
    noise = db.Column(db.String(20), nullable=False)
    handle = db.Column(db.String(20), nullable=False)
    guaranty = db.Column(db.String(20), nullable=False)
    control_unit = db.Column(db.String(20), nullable=False)
    power = db.Column(db.String(20), nullable=False)
    chambers = db.Column(db.String(20), nullable=False)
    doors = db.Column(db.String(20), nullable=False)
    useful_volume = db.Column(db.String(20), nullable=False)
    useful_volume_ref = db.Column(db.String(20), nullable=False)
    useful_volume_freezer = db.Column(db.String(20), nullable=False)
    voltage_frequency = db.Column(db.String(20), nullable=False)
    energy_consumption = db.Column(db.String(20), nullable=False)
    coolant = db.Column(db.String(20), nullable=False)
    series = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.String(20), nullable=False)
    defrosting_system = db.Column(db.String(20), nullable=False)
    shelves = db.Column(db.String(20), nullable=False)
    barriers = db.Column(db.String(20), nullable=False)
    baskets = db.Column(db.String(20), nullable=False)
    inserts = db.Column(db.String(20), nullable=False)
    stoppers = db.Column(db.String(20), nullable=False)
    freezer_temp = db.Column(db.String(20), nullable=False)
    freezing_capacity = db.Column(db.String(20), nullable=False)
    freezer_parts = db.Column(db.String(20), nullable=False)
    size_without = db.Column(db.String(20), nullable=False)
    size_with = db.Column(db.String(20), nullable=False)
    weight_without = db.Column(db.String(20), nullable=False)
    weight_with = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.String(200), nullable=False)
    image_path = db.Column(db.String(50), nullable=False, unique=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    prods = Prod.query.all()
    return render_template("index.html", prods=prods)


@app.route("/panel", methods=["POST", "GET"])
def panel():
    if request.method == "POST":
        file = request.files['image']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prod = Prod(model=request.form["model"],
                    producer=request.form["producer"],
                    price=request.form["price"],
                    width=request.form["width"],
                    depth=request.form["depth"],
                    height=request.form["height"],
                    weight=request.form["weight"],
                    volume=request.form["volume"],
                    service=request.form["service"],
                    country=request.form["country"],
                    category=request.form["category"],
                    colling=request.form["colling"],
                    color=request.form["color"],
                    energy_efficiency=request.form["energy-efficiency"],
                    compressors=request.form["compressors"],
                    noise=request.form["noise"],
                    handle=request.form["handle"],
                    guaranty=request.form["guaranty"],
                    control_unit=request.form["control-unit"],
                    power=request.form["power"],
                    chambers=request.form["chambers"],
                    doors=request.form["doors"],
                    useful_volume=request.form["useful-volume"],
                    useful_volume_ref=request.form["useful-volume-ref"],
                    useful_volume_freezer=request.form["useful-volume-freezer"],
                    voltage_frequency=request.form["voltage-frequency"],
                    energy_consumption=request.form["energy-consumption"],
                    coolant=request.form["coolant"],
                    series=request.form["series"],
                    temperature=request.form["temperature"],
                    defrosting_system=request.form["defrosting-system"],
                    shelves=request.form["shelves"],
                    barriers=request.form["barriers"],
                    baskets=request.form["baskets"],
                    inserts=request.form["inserts"],
                    stoppers=request.form["stoppers"],
                    freezer_temp=request.form["freezer-temp"],
                    freezing_capacity=request.form["freezing-capacity"],
                    freezer_parts=request.form["freezer-parts"],
                    size_without=request.form["size-without"],
                    size_with=request.form["size-with"],
                    weight_without=request.form["weight-without"],
                    weight_with=request.form["weight-with"],
                    description=request.form["description"],
                    image_path="/uploads/"+filename
                    )
        try:
            db.session.add(prod)
            db.session.commit()
            return redirect("/panel")
        except:
            return "Ошибка"
    else:
        return render_template("panel.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(login=request.form['login'], phone_number=request.form['phone_number'], password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        except:
            return "Ошибка"
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(login=request.form["login"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            flash(f"Поздравляем {request.form['login']} Вы успешно авторизованы!", "success")
            return redirect("/")
    return render_template("login.html")


@app.route("/product")
def product():
    prod_id = request.args["id"]
    if prod_id.isdigit():
        prod = Prod.query.get(prod_id)
        if prod:
            return render_template("product.html", prod=prod)
    return "404"


if __name__ == "__main__":
    app.run(debug=True)
