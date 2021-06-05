from flask import Flask, render_template, url_for, redirect
import os
from display import displayDataLineage

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
            
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

ddl = displayDataLineage()

lineage = ddl.showAttributeLineage()
deltaLineage = ddl.showDeltaLineage()
edgeList = ddl.getEdgeListBFS()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', lineage=lineage)

@app.route('/attributeLineage')
def attributeLineage():
    return render_template('attributeLineage.html', lineage=lineage, edgeList=edgeList)
    
@app.route('/attributeDeltaLineage')
def attributeDeltaLineage():
    return render_template('attributeDeltaLineage.html', lineage=deltaLineage)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)