from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, FileField
from wtforms.validators import DataRequired

class TripForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    location = StringField('Местоположение', validators=[DataRequired()])
    latitude = FloatField('Широта')
    longitude = FloatField('Долгота')
    description = TextAreaField('Описание', validators=[DataRequired()])
    cost = FloatField('Стоимость')
    image = FileField('Изображение')
    transport_rating = IntegerField('Оценка удобства передвижения')
