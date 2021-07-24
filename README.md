# algorithms-implementations

The main branch of this repo will hold the base working application which can work standalone to visualize the quality/drift of the domain objects across their lineage, involved in a data pipeline

However, since the core of this work is based on breadth first search of the nodes of a directed graph, it is strongly advised to avoid overlapping edges emanating from & descending on multiple nodes 

This is also needed to allow a clear view of the edge levels showing the percentage difference in the data

Do not forget to create your own credentials.py with two functions simply returning the database username and credentials and then create a .pyc file out of it, the path to this .pyc file should be in your config.txt 