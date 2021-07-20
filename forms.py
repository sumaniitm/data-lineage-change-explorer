from flask_wtf import FlaskForm, Form
from wtforms import SubmitField, DateField, SelectField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired
from dbUtil import DbUtil


class LineageDates(FlaskForm):
    du = DbUtil()
    levels = du.levels.split(',')
    for i in levels:
        choice = du.getdropdowndata(i)
        locals()['level_%s' % i] = SelectField(u'%s' % i, choices=choice)
    #choice = du.getdropdowndata('report_date')
    #level_report_date = SelectField(u'Report Date', choices=choice)
    # lineagerequestedfordate = DateField('Lineage Requested For Date', validators=[DataRequired()])
    # lineagecomparedwithdate = DateField('Lineage Compared with Date', validators=[DataRequired()])


class LevelForm(FlaskForm):
    """A form for one or more addresses"""
    levelnames = FieldList(FormField(LineageDates), min_entries=1)
    submit = SubmitField('Get Lineage')
