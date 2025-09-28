#                               !Das Vibe Code Paradox!
# Ein Admin Interface soll sicher sein --> Das ist aber schwer  -> KI macht den Job --> Das ist Unsicher -> Also setzte ich 
# die nächsten 5 stunden hin und richte den Code
from flask import Flask, redirect, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_geheimes_passwort'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meine_datenbank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ User Auth ------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ Tabellen ------------------
class Verkaeufer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Inventar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stueckzahl = db.Column(db.Integer, nullable=False)
    preis = db.Column(db.Float)

class Verkaeufe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    objekt_id = db.Column(db.Integer, db.ForeignKey('inventar.id'))
    anzahl = db.Column(db.Integer)
    preisPerPiece = db.Column(db.Float)
    date = db.Column(db.String(50))
    description = db.Column(db.String(200))
    seller1_id = db.Column(db.Integer, db.ForeignKey('verkaeufer.id'))
    seller2_id = db.Column(db.Integer, db.ForeignKey('verkaeufer.id'))

# ------------------ Gesicherte Views ------------------
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        return super(SecureAdminIndexView, self).index()

# ------------------ Flask-Admin Setup ------------------
admin = Admin(app, name="Sicheres Dashboard", index_view=SecureAdminIndexView(), template_mode="bootstrap4")
admin.add_view(SecureModelView(Verkaeufer, db.session))
admin.add_view(SecureModelView(Inventar, db.session))
admin.add_view(SecureModelView(Verkaeufe, db.session))

# ------------------ Routen für Login ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("admin.index"))
        return "Login fehlgeschlagen!"
    return render_template("godmode.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ------------------ Start ------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Erstes Admin-Konto anlegen, wenn keins existiert
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin")
            admin_user.set_password("starkes_passwort")
            db.session.add(admin_user)
            db.session.commit()

    app.run(debug=True)
