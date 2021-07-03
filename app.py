from flask import Flask, render_template, url_for, redirect, flash
import os
from display import displayDataLineage
import forms

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
            
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

ddl = displayDataLineage()

lineage,edgeList = ddl.showAttributeLineage()
deltaEdgeLineage = ddl.showDeltaLineage()

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = forms.LineageRequestedForDate()
    if form.validate_on_submit():
        print('within validate')
        return redirect(url_for('index'))
    flash('Incorrect Date input')
    print('outside validate')
    print(form.errors)
    return render_template('home.html', form=form)

@app.route('/index')
def index():
    return render_template('index.html', lineage=lineage)

@app.route('/attributeLineage')
def attributeLineage():
    return render_template('attributeLineage.html', lineage=lineage, edgeList=edgeList)
    
@app.route('/attributeDeltaLineage')
def attributeDeltaLineage():
    return render_template('attributeDeltaLineage.html', lineage=lineage, deltaEdgeLineage=deltaEdgeLineage)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)