from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required, current_user
from datetime import date
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = os.urandom(15)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_view = 'login'


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

    orders = db.relationship('Order', back_populates='prod')

    reviews = db.relationship('Review', back_populates='prod')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(13), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20))

    orders = db.relationship('Order', back_populates='user')

    reviews = db.relationship('Review', back_populates='user')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_phone_number = db.Column(db.String(20), nullable=False)
    user_email = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="на рассмотрении")
    date = db.Column(db.String(10), nullable=False)

    prod_id = db.Column(db.Integer, db.ForeignKey('prod.id'))
    prod = db.relationship('Prod', back_populates='orders')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='orders')


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(10), nullable=False)
    end_date = db.Column(db.String(10), nullable=False)

    prod_id = db.Column(db.Integer, db.ForeignKey('prod.id'))
    prod = db.relationship('Prod', backref='sale')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    grade = db.Column(db.Integer, nullable=False, default=1)
    text = db.Column(db.String(500), default="")

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', backref='order')

    prod_id = db.Column(db.Integer, db.ForeignKey('prod.id'))
    prod = db.relationship('Prod', back_populates='reviews')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='reviews')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["POST", "GET"])
def index():
    prods = Prod.query.all()
    producers = []
    for prod in prods:
        if prod.producer not in producers:
            producers.append(prod.producer)
    if request.method == "POST":
        if request.form["button"] == "search":
            new_prods = []
            search = request.form["search"]
            for prod in prods:
                if search in prod.model:
                    new_prods.append(prod)
            return render_template("index.html", prods=new_prods, producers=producers)
        if request.form["button"] == "filters":
            picked_producer = ""
            if "producer" in request.form:
                picked_producer = request.form["producer"]
                for prod in prods:
                    if prod.producer != picked_producer:
                        prods.remove(prod)
            min_price, max_price = 0, max(prods, key=lambda prod: prod.price).price
            f1, f2 = False, False
            if request.form["max_price"]:
                max_price = request.form["max_price"]
                f1 = True
            if request.form["min_price"]:
                min_price = request.form["min_price"]
                f2 = True
            for prod in prods:
                if not int(min_price) <= prod.price <= int(max_price):
                    prods.remove(prod)
            return render_template("index.html", prods=prods, producers=producers, picked_producer=picked_producer, f1=f1, f2=f2, min_price=min_price, max_price=max_price)
        if request.form["button"] == "drop":
            render_template("index.html", prods=prods, producers=producers)
    if "sort" in request.args:
        if request.args["sort"] == "cheap":
            prods.sort(key=lambda prod: prod.price)
            return render_template("index.html", prods=prods, producers=producers)
        elif request.args["sort"] == "expensive":
            prods.sort(key=lambda prod: prod.price, reverse=True)
            return render_template("index.html", prods=prods, producers=producers)
    return render_template("index.html", prods=prods, producers=producers)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(login=request.form['login'], phone_number=request.form['phone_number'], password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        except Exception as e:
            print(e)
            return "Ошибка"
    return render_template('register.html')


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        try:
            remember = request.form["remember"]
        except:
            remember = False
        user = User.query.filter_by(login=request.form["login"]).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            try:
                next_page = request.args["next"]
                login_user(user, remember=remember)
                return redirect(next_page)
            except:
                login_user(user, remember=remember)
                return redirect("/")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/cub", methods=["POST", "GET"])
@login_required
def cub():
    if request.method == 'POST':
        user = User.query.get(request.form["user_id"])
        if user and bcrypt.check_password_hash(user.password, request.form["old_password"]):
            user.password = bcrypt.generate_password_hash(request.form['new_password']).decode('utf-8')
            db.session.commit()
            flash("Пароль успешно изменён!")
        return redirect("/")
    if current_user.orders:
        return render_template("cub.html", orders=current_user.orders)
    return render_template("cub.html")


@app.route("/order", methods=["POST", "GET"])
@login_required
def order():
    if current_user.role:
        return redirect("/")
    prod_id = request.args["id"]
    if prod_id.isdigit():
        prod = Prod.query.get(prod_id)
        if prod:
            if request.method == "POST":
                try:
                    dat = date.today()
                    order = Order(user_phone_number=request.form["phone"],
                                  user_email=request.form["email"],
                                  date=str(dat.day) + "." + str(dat.month) + "." + str(dat.year),
                                  user_id=current_user.id,
                                  prod_id=prod_id)
                    db.session.add(order)
                    db.session.commit()
                    return redirect("/")
                except:
                    return "Ошибка создания азказа"
            return render_template("order.html", prod=prod)
    return "404"


@app.route("/product", methods=["POST", "GET"])
def product():
    prod_id = request.args["id"]
    if prod_id.isdigit():
        prod = Prod.query.get(prod_id)
        if prod:
            if request.method == "POST":
                dat = date.today()
                review = Review(date=str(dat.day) + "." + str(dat.month) + "." + str(dat.year),
                                grade=request.form["rating"], text=request.form["review"], prod_id=prod_id,
                                prod=Prod.query.get(prod_id), user_id=current_user.id,
                                user=User.query.get(current_user.id))
                prod_rating = 0.0
                for i in prod.reviews:
                    prod_rating += i.grade
                if len(prod.reviews) != 0:
                    prod.rating = round(prod_rating / len(prod.reviews), 2)
                try:
                    db.session.add(review)
                    db.session.commit()
                    return redirect(f"/product?id={prod_id}")
                except Exception as e:
                    print(e)
                    return redirect(f"/product?id={prod_id}")
            reviews = Review.query.all()
            page = 1
            max_page = int(len(reviews) / 10 + 0.9)
            if "page" in request.args:
                page = int(request.args["page"])
            reviews = reviews[(page - 1) * 10:(page - 1) * 10 + 10]
            flag = False
            if current_user.is_active:
                for order in current_user.orders:
                    if order.user.id == current_user.id and order.status == "принят":
                        flag = True
            return render_template("product.html", prod=prod, reviews=reviews, page=page, max_page=max_page, flag=flag)
    return "404"


@app.route("/panel/orders", methods=["POST", "GET"])
@login_required
def orders():
    if not current_user.role:
        return redirect("/")
    if request.method == "POST":
        if request.form["accept"][0] == "1":
            try:
                order = Order.query.get(request.form["accept"][1:])
                order.status = "принят"
                db.session.commit()
            except Exception as e:
                print(e)
        else:
            try:
                order = Order.query.get(request.form["accept"][1:])
                order.status = "отказано"
                db.session.commit()
            except Exception as e:
                print(e)
        return redirect("/panel/orders")
    orders = Order.query.all()
    return render_template("orders.html", orders=orders)


@app.route("/panel/sales", methods=["POST", "GET"])
@login_required
def sales():
    if not current_user.role:
        return redirect("/")
    if request.method == "POST":
        if request.form["button"][0:6] == "create":
            if int(request.form["amount"]) > 80:
                flash('Скидка не может быть больше 80%!', 'success')
                return redirect("/panel/sales")
            sale = Sale(amount=request.form["amount"], prod=Prod.query.get(request.form["product"]),
                        prod_id=request.form["product"])
            try:
                new_price = round(sale.prod.price * (1 - int(sale.amount) / 100), 2)
                sale.prod.price = new_price
                db.session.add(sale)
                db.session.commit()
            except Exception as e:
                print(e)
        if request.form["button"][0:6] == "delete":
            sale = Sale.query.get([request.form["button"][6:]])
            try:
                new_price = round(sale.prod.price / (1 - int(sale.amount) / 100), 2)
                sale.prod.price = new_price
                db.session.delete(sale)
                db.session.commit()
            except Exception as e:
                print(e)
        return redirect("/panel/sales")
    prods = Prod.query.all()
    sales = Sale.query.all()
    return render_template("sales.html", prods=prods, sales=sales)


@app.route("/panel/products", methods=["POST", "GET"])
@login_required
def products():
    if not current_user.role:
        return redirect("/")
    if request.method == "POST":
        if request.form["button"] == "create_product":
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
                        image_path="/uploads/" + filename
                        )
            try:
                db.session.add(prod)
                db.session.commit()
                return redirect("/panel/products")
            except Exception as e:
                print(e)
                return "Ошибка"
        elif request.form["button"] == "delete":
            prod = Prod.query.get(request.form["product"])
            try:
                db.session.delete(prod)
                db.session.commit()
                return redirect("/panel/products")
            except:
                return "Ошибка удаления из базы данных"
    else:
        prods = Prod.query.all()
        return render_template("products.html", prods=prods)


@app.route("/panel")
@login_required
def panel():
    if not current_user.role:
        return redirect("/")
    return render_template("panel.html")


if __name__ == "__main__":
    app.run(debug=True)
