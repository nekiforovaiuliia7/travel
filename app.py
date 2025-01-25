from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime
from forms import TripForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_diary.db'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Модели и формы (см. выше)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    trips = Trip.query.order_by(Trip.created_at.desc()).all()
    return render_template('index.html', trips=trips)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create_trip', methods=['GET', 'POST'])
@login_required
def create_trip():
    form = TripForm()
    if form.validate_on_submit():
        title = form.title.data
        location = form.location.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        description = form.description.data
        cost = form.cost.data
        transport_rating = form.transport_rating.data
        image = photos.save(form.image.data) if form.image.data else None

        trip = Trip(
            title=title,
            location=location,
            latitude=latitude,
            longitude=longitude,
            description=description,
            cost=cost,
            image=image,
            transport_rating=transport_rating,
            author=current_user
        )
        db.session.add(trip)
        db.session.commit()
        flash('Запись о путешествии успешно создана!', 'success')
        return redirect(url_for('index'))
    return render_template('create_trip.html', form=form)

@app.route('/trip/<int:trip_id>')
def view_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    return render_template('trip.html', trip=trip)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
