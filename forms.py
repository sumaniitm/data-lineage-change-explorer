from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class LineageDates(FlaskForm):
    lineagerequestedfordate = DateField('Lineage Requested For Date', validators=[DataRequired()])
    lineagecomparedwithdate = DateField('Lineage Compared with Date', validators=[DataRequired()])
    submit = SubmitField('Get Lineage')
