# Explore changes along the lineage of a data entity

The main branch of this repo will hold the base working application which can work standalone to visualize the quality/drift of the data entities across their lineage.
The current version of the docker image can be found in
https://hub.docker.com/layers/171284147/sumaniitm/data_lineage_change_explorer/v0_1/images/sha256-72b925fcfbe83ba1aaa6cd1970ff4a193f4f314f80d1fb0eb3bef8d7ab63ca68?context=repo

The image is tested to be working on a Macbook Pro with PostgreSQL installed locally

However, since the core of this work is based on breadth first search of the nodes of a directed graph, overlapping edges emanating from & descending on multiple nodes will not be displayed
This is needed to allow a clear view of the edge levels showing the percentage difference in the data

Do not forget to create your own credentials.py with two functions simply returning the database username and credentials and then create a .pyc file out of it, the path to this .pyc file should be in your config.txt 

Main landing page

<img width="829" alt="gango3" src="https://user-images.githubusercontent.com/35261783/131540047-24a5ff7e-d9c5-421d-8774-412820cc274e.png">

Intermediate page showing the list of entities (based on the users entries in config.txt), with navigation link

<img width="931" alt="gango6" src="https://user-images.githubusercontent.com/35261783/132115190-57c69031-e7d2-4d76-8a8d-656b26d012c0.png">

Final Output showing the changes in the source, transformations and destination of the selected (from the intermediate page) data entity

<img width="1777" alt="gango7" src="https://user-images.githubusercontent.com/35261783/132115214-9fde341b-7876-42db-a849-b37519292513.png">

