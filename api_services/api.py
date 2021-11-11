"""
This module will contain the api to retrieve the lineage graph with the deltas of the data entities

The inputs to the module are as follows
1. path to the configuration file; e.g./Users/sumangangopadhyay/data-lineage-change-explorer/config.txt
    1.1. The config file should have the relevant entries
2. either a sqlalchemy create_engine connect object for PostgreSQL database or a snowflake connector connect object for
Snowflake database
3. the path of the edge (current and past lookup) json files
4. the location where the vertex json files should be built by the module

Returns
    A dictionary with source, destination and the delta of the source and destination data entities
"""
from display import DisplayDataLineage


def get_lineage_with_delta():
    pass

