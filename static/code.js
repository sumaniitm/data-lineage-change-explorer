/*
function connected_edges(d){
	var edges = svgGroup.selectAll(".edge");
        var list_selected = {}
	return list_selected;
}
*/

function connected_nodes(d){
	var edges = svgGroup.selectAll(".edge");
        var selected = {}
	edges._groups[0].forEach(function(e){
		var source_id = e.id.split('-')[0]
                var destination_id = e.id.split('-')[1]
		if (source_id == d.id){
                	selected[destination_id] = '';
		}
		if (destination_id == d.id){
                	selected[source_id] = '';
		}
	});
	return selected;
}

// Create the input graph
var g = new dagreD3.graphlib.Graph()
  .setGraph({'align': 'UL', 'rankdir': 'RL', 'ranker': 'longest-path'})
  .setDefaultEdgeLabel(function() { return {}; });

// Here we're setting nodeclass, which is used by our custom drawNodes function
// below.


for(index in nodes_list){
	g.setNode(
		nodes_list[index].id,
		{label: nodes_list[index].name, class: "node", id: nodes_list[index].id}
	);	
}

g.nodes().forEach(function(v) {
  var node = g.node(v);
  // Round the corners of the nodes
  node.rx = node.ry = 5;
});

// Set up edges, no special attributes.

for(index in edges_list){
	//temporarily switching it to check it out, revert it back.
	g.setEdge(
		edges_list[index].source,
		edges_list[index].destination,
		{
			curve: d3.curveBasis ,
			id:String(edges_list[index].source)+"-"+String(edges_list[index].destination),
			class: "edge"
		}
	);
}

// Create the renderer
var render = new dagreD3.render();

// Set up an SVG group so that we can translate the final graph.
var svg = d3.select("svg"),
svgGroup = svg.append("g");

// Run the renderer. This is what draws the final graph.
render(d3.select("svg g"), g);

// Center the graph
var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
svg.attr("height", g.graph().height + 40);


nodes = svgGroup.selectAll(".node")
edges = svgGroup.selectAll(".edge")

nodes.on("click", function(d) {
	d3.event.stopPropagation();
	nodes._groups[0].forEach(function(n){
			n.classList.add("visible");
			n.classList.remove("invisible");
	});
	edges._groups[0].forEach(function(e){
			e.classList.add("visible");
			e.classList.remove("invisible");
	});
	clicked_elem = this;
	clicked_elem.classList.add("selected");
        selected_nodes = connected_nodes(clicked_elem);
        nodes._groups[0].forEach(function(n){
		if(!(n.id in selected_nodes || n.id == clicked_elem.id)){
			n.classList.add("invisible");
			n.classList.remove("visible");
		}	
	});
	edges._groups[0].forEach(function(e){
		if(!((e.id.split('-')[0] == clicked_elem.id) || (e.id.split('-')[1] == clicked_elem.id))){
			e.classList.add("invisible");
			e.classList.remove("visible");
		}	
	});
});


svg.on("click", function(){
	nodes._groups[0].forEach(function(n){
			n.classList.add("visible");
			n.classList.remove("invisible");
                        n.classList.remove("selected");
	});
	edges._groups[0].forEach(function(e){
			e.classList.add("visible");
			e.classList.remove("invisible");
	});
});
