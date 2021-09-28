"""
This piece of code declares the main form class LineageDates, which is a collection of wtforms SelectFields. These
hold the data of the dropdown for the various levels of aggregation. This collection is then used in the entry point
of the flask app as a list of form fields, LevelForm
"""

from flask_wtf import FlaskForm, Form
from wtforms import SubmitField, DateField, SelectField
from wtforms.fields import FormField, FieldList
from buildjsons import BuildJsons
import configparser as cp


class LineageDates(FlaskForm):
    du = BuildJsons('snowflake')
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
            choice.append('N/A')
            locals()['level_%s' % i] = SelectField(u'%s' % i, choices=choice, default='N/A')


class LevelForm(FlaskForm):
    levelnames = FieldList(FormField(LineageDates), min_entries=1)
    submit = SubmitField('Get Lineage')
