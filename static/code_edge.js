// Create the input graph
var g = new dagreD3.graphlib.Graph()
  .setGraph({'align': 'UL', 'rankdir': 'RL', 'ranker': 'longest-path'})
  .setDefaultEdgeLabel(function() { return {}; });

// Here we're setting nodeclass, which is used by our custom drawNodes function
// below.

for(index in nodes_list){
	g.setNode(
		nodes_list[index].id,
		{label: nodes_list[index].name, class: "node", id: nodes_list[index].id, height: 50, width: 200, labelStyle: "font-size: 0.90em"}
	);	
}

g.nodes().forEach(function(v) {
  var node = g.node(v);
  // Round the corners of the nodes
  node.rx = node.ry = 5;
  //node.width = 180;
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
			label: edges_list[index].label,
			labelStyle: "font-size: 0.70em",
			class: "edge",
			height: 30,
			width: 50
		}
	);
}

// Set up an SVG group so that we can translate the final graph.
//var svg = d3.selectAll("svg");
var svg = d3.selectAll("svg"),
    inner = svg.selectAll("g");

// Create the renderer
var render = new dagreD3.render();

// Run the renderer. This is what draws the final graph.
//render(d3.select("svg"), g);
render(svg, g);

// Center the graph
svg.attr("width", g.graph().width + 10);
svg.attr("height", g.graph().height + 200);
var xCenterOffset = (svg.attr("width") - g.graph().width) / 2;
//svgGroup.attr("transform", "translate(" + xCenterOffset + ", 50)");
svg.attr("transform", "translate(" + xCenterOffset + ", 100)");

console.log(g)

