"""
This class acts as the entry point to the flask application. the home page is the main landing page where the user can
see/choose the levels of aggregation as per the entries in the config.txt. Then comes the intermediate page which
displays the navigable links to the lineage of the various data entities as defined in config.txt. Finally on clicking
any of these navigable links from the intermediate page, the user is taken to the detailed page of the entity which
displays the changes of the entity along its lineage. The form data is passed from home page to index to the final page
"""

from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages, request
from display import DisplayDataLineage
from baseDbUtil import BaseDbUtil
from buildjsons import BuildJsons
import forms
import configparser as cp
import ast

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
            
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

config = cp.ConfigParser()
config.read('config.txt')
database_to_connect = config.get('db-settings', 'database')
bj = BuildJsons(database_to_connect)
du = BaseDbUtil()
levels = du.levels.split(',')
number_of_entities = int(du.number_of_entities)
entity_list = du.entity_list.split(',')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = forms.LevelForm()
    date_column_name = du.date_column_name
    if form.is_submitted():
        if form.validate_on_submit():
            bj.buildvertexjson()
            levels_from_form = form.levelnames.data
            list_of_form_data = levels_from_form[0]
            print(list_of_form_data)
            del list_of_form_data['csrf_token']
            bj.buildedgejson(list_of_form_data, mode='Future')
            bj.buildedgejson(list_of_form_data, mode='Past')
            list_of_form_data = {k.replace('level_', ''): v.replace('level_', '') for k, v in list_of_form_data.items()}
            return redirect(url_for('index', list_of_form_data=list_of_form_data))
        else:
            flash('Incorrect Date input')
    return render_template('home.html', form=form, date_column_name=date_column_name)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', entity_list=entity_list
                           , list_of_form_data=ast.literal_eval(request.args.get('list_of_form_data')))


@app.route('/attribute_delta_lineage/<entity>', methods=['GET', 'POST'])
def attribute_delta_lineage(entity):
    print(entity)
    delta_edge_lineage = []
    lineage = []
    for i in range(number_of_entities):
        if entity == entity_list[i]:
            json_edge_file_name_with_path = """json_files/edges_entity_{0}.json""".format(i + 1)
            json_lookup_file_name_with_path = """json_files/lookupPast_entity_{0}.json""".format(i + 1)
            vertex_file_name_with_path = """json_files/vertices_entity_{0}.json""".format(i + 1)
            ddl = DisplayDataLineage(vertex_json_file=vertex_file_name_with_path,
                                     edge_json_file=json_edge_file_name_with_path,
                                     lookup_json_file=json_lookup_file_name_with_path)
            delta_edge_lineage.append(ddl.show_delta_lineage())
            lineage.append(ddl.show_attribute_lineage())
    nodes_edges = zip(lineage, delta_edge_lineage)
    list_of_tuples = list(nodes_edges)
    return render_template('attributeDeltaLineage.html', list_of_tuples=list_of_tuples, entity=entity
                           , list_of_form_data=ast.literal_eval(request.args.get('list_of_form_data')))


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)
