from flask_wtf import FlaskForm, Form
from wtforms import SubmitField, DateField, SelectField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired
from dbUtil import DbUtil
import configparser as cp

class LineageDates(FlaskForm):
    du = DbUtil()
    config = cp.ConfigParser()
    config.read('config.txt')
    date_column_name = config.get('db-settings', 'date_column_name')
    levels = du.levels.split(',')
    for i in levels:
        choice = du.getdropdowndata(i)
        if date_column_name == i:
            locals()['level_future_%s' % i] = SelectField(u'future_%s' % i, choices=choice)
            locals()['level_past_%s' % i] = SelectField(u'past_%s' % i, choices=choice)
        else:
            locals()['level_%s' % i] = SelectField(u'%s' % i, choices=choice)
    #choice = du.getdropdowndata('report_date')
    #level_report_date = SelectField(u'Report Date', choices=choice)
    # lineagerequestedfordate = DateField('Lineage Requested For Date', validators=[DataRequired()])
    # lineagecomparedwithdate = DateField('Lineage Compared with Date', validators=[DataRequired()])


class LevelForm(FlaskForm):
    """A form for one or more addresses"""
    levelnames = FieldList(FormField(LineageDates), min_entries=1)
    submit = SubmitField('Get Lineage')
