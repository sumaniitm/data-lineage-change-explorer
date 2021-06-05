var nodes_list = [
	{'name':'Market Customer Demand', id: 0},
	{'name':'Customer Demand', id: 1}, 
	{'name':'Direct Demand', id: 2}, 
	{'name':'Predicted Demand', id: 3}, 
	{'name':'Sales Order', id: 4}, 
	{'name':'Remaining Forecast', id: 5}, 
	{'name':'Model Outputs', id: 6}, 
];

var edges_list = [
	{'source': 1, 'destination': 0},
	{'source': 2, 'destination': 1},
	{'source': 3, 'destination': 1},
	{'source': 4, 'destination': 2},
	{'source': 5, 'destination': 2},
	{'source': 6, 'destination': 3}
];