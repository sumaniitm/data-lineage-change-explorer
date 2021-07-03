from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired

class LineageRequestedForDate(FlaskForm):
    lineagerequestedfordate = DateField('Lineage Requested For Date', validators=[DataRequired()])
    submit = SubmitField('Get Lineage')