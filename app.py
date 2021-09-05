from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages
from display import displayDataLineage
from dbUtil import DbUtil
from buildjsons import BuildJsons
import forms
import configparser as cp

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
            
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

#ddl = displayDataLineage()
bj = BuildJsons()
du = DbUtil()
levels = du.levels.split(',')
number_of_entities = int(du.number_of_entities)
entity_list = du.entity_list.split(',')

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = forms.LevelForm()
    #list_of_form_data = {}
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
            return redirect(url_for('index'))
        else:
            flash('Incorrect Date input')
    return render_template('home.html', form=form, date_column_name=date_column_name)


#lineage, edgeList = ddl.showAttributeLineage()
#deltaEdgeLineage = ddl.showDeltaLineage()
#totalNumOfNodes = len(lineage)


@app.route('/index')
def index():
    return render_template('index.html', entity_list=entity_list)


#@app.route('/attributeLineage')
#def attributeLineage():
#    return render_template('attributeLineage.html', lineage=lineage, edgeList=edgeList, totalNumOfNodes=totalNumOfNodes)


@app.route('/attributeDeltaLineage/<entity>', methods=['GET', 'POST'])
def attributeDeltaLineage(entity):
    config = cp.ConfigParser()
    print(entity)
    config.read('config.txt')
    deltaEdgeLineage = []
    lineage = []
    for i in range(number_of_entities):
        if entity == entity_list[i]:
            jsonEdgeFileNameWithPath = """json_files/edges_entity_{0}.json""".format(i + 1)
            jsonLookupFileNameWithPath = """json_files/lookupPast_entity_{0}.json""".format(i + 1)
            vertexFileNameWithPath = """json_files/vertices_entity_{0}.json""".format(i + 1)
            ddl = displayDataLineage(vertexJsonFile=vertexFileNameWithPath, edgeJsonFile=jsonEdgeFileNameWithPath, lookupJsonFile=jsonLookupFileNameWithPath)
            deltaEdgeLineage.append(ddl.showDeltaLineage())
            lineage.append(ddl.showAttributeLineage())
    nodes_edges = zip(lineage, deltaEdgeLineage)
    list_of_tuples = list(nodes_edges)
    return render_template('attributeDeltaLineage.html', list_of_tuples=list_of_tuples, entity=entity)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)