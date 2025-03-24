from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    meme = FileField('Izvēlies MEME attēlu', validators=[DataRequired()])
    submit = SubmitField('Augšupielādēt')