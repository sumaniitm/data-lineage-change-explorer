import airflow
from airflow.plugins_manager import AirflowPlugin
from flask_admin import BaseView, expose
from flask_appbuilder import BaseView as AppBuilderBaseView
from flask_appbuilder import has_access
from flask_admin.base import MenuLink
from flask import Flask, render_template, url_for, redirect, Blueprint
import os
from display import displayDataLineage

class customAppLauncher(AppBuilderBaseView):
    ddl = displayDataLineage()
    lineage,edgeList = ddl.showAttributeLineage()
    deltaEdgeLineage = ddl.showDeltaLineage()

    @expose('/')
    def list(self):
        ddl = displayDataLineage()
        lineage,edgeList = ddl.showAttributeLineage()
        return self.render_template('index.html', lineage=lineage)

    @expose('/attributeLineage')
    def attributeLineage(self):
        ddl = displayDataLineage()
        lineage,edgeList = ddl.showAttributeLineage()
        return self.render_template('attributeLineage.html', lineage=lineage, edgeList=edgeList)
    
    @expose('/attributeDeltaLineage')
    def attributeDeltaLineage(self):
        ddl = displayDataLineage()
        lineage,edgeList = ddl.showAttributeLineage()
        deltaEdgeLineage = ddl.showDeltaLineage()
        return self.render_template('attributeDeltaLineage.html', lineage=lineage, deltaEdgeLineage=deltaEdgeLineage)

bp = Blueprint(
        "Lineages", __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='')

class AirflowCustomLauncher(AirflowPlugin):
    name = "Lineages"
    app = customAppLauncher()
    app_launcher_package = {
            "name": "Custom App",
            "category": "Lineages",
            "view": app
            }
    appbuilder_views = [app_launcher_package]
    flask_blueprints = [bp]

