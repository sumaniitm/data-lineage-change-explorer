from flask import Flask, render_template
import os
from display import displayDataLineage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
print(__name__)

ddl = displayDataLineage()

lineage = ddl.showAttributeLineage()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', lineage=lineage)

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)