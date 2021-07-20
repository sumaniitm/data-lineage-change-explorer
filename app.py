from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages
from display import displayDataLineage
from dbUtil import DbUtil
import forms

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
            
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

ddl = displayDataLineage()
du = DbUtil()
levels = du.levels.split(',')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = forms.LevelForm()
    list_of_form_data = []
    for i in levels:
        list_of_form_data.append('level_' + i)
    # for n in range(len(list_of_form_data)):
    #    print(list_of_form_data[n])
    if form.is_submitted():
        if form.validate_on_submit():
            du.buildvertexjson()
            # lineage_requested_on = form.lineagerequestedfordate.data
            # du.buildedgejson(lineage_requested_on=lineage_requested_on, mode='Future')
            # lineage_tobe_compared_with = form.lineagecomparedwithdate.data
            # du.buildedgejson(lineage_requested_on=lineage_tobe_compared_with, mode='Past')
            return redirect(url_for('index'))
        else:
            flash('Incorrect Date input')
    return render_template('home.html', form=form, list_of_form_data=list_of_form_data)


lineage, edgeList = ddl.showAttributeLineage()
deltaEdgeLineage = ddl.showDeltaLineage()
totalNumOfNodes = len(lineage)


@app.route('/index')
def index():
    return render_template('index.html', lineage=lineage)


@app.route('/attributeLineage')
def attributeLineage():
    return render_template('attributeLineage.html', lineage=lineage, edgeList=edgeList, totalNumOfNodes=totalNumOfNodes)


@app.route('/attributeDeltaLineage')
def attributeDeltaLineage():
    return render_template('attributeDeltaLineage.html', lineage=lineage, deltaEdgeLineage=deltaEdgeLineage, totalNumOfNodes=totalNumOfNodes)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)