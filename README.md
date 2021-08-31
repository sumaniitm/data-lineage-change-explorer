# Explore changes along the lineage of a data entity

The main branch of this repo will hold the base working application which can work standalone to visualize the quality/drift of the data entities across their lineage

However, since the core of this work is based on breadth first search of the nodes of a directed graph, overlapping edges emanating from & descending on multiple nodes will not be displayed
This is needed to allow a clear view of the edge levels showing the percentage difference in the data

Do not forget to create your own credentials.py with two functions simply returning the database username and credentials and then create a .pyc file out of it, the path to this .pyc file should be in your config.txt 

Main landing page

<img width="829" alt="gango3" src="https://user-images.githubusercontent.com/35261783/131540047-24a5ff7e-d9c5-421d-8774-412820cc274e.png">

Final Output showing the changes in the source, transformations and destination of a data entity

<img width="999" alt="gango4" src="https://user-images.githubusercontent.com/35261783/131539857-c233e41c-fb74-42aa-a85f-a555032cb261.png">

