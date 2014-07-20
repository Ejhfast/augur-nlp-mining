var margin = {top: -5, right: -5, bottom: -5, left: -5},
    width = 640 - margin.left - margin.right,
    height = 480 - margin.top - margin.bottom;


var zoom = d3.behavior.zoom()
    .scaleExtent([0.1, 20])
    .on("zoom", zoomed);

var drag = d3.behavior.drag()
    .origin(function(d) { return d; })
    .on("dragstart", dragstarted)
    .on("drag", dragged)
    .on("dragend", dragended);


function zoomed() {
  container.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}

function dragstarted(d) {
  d3.event.sourceEvent.stopPropagation();
  d3.select(this).classed("dragging", true);
}

function dragged(d) {
  d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
}

function dragended(d) {
  d3.select(this).classed("dragging", false);
}

var width = 640,
    height = 480;

var color = d3.scale.category20();

var force = d3.layout.force()
    .linkDistance(15)
    .linkStrength(2)
    .gravity(0.05)
    .size([width, height]);

var svg = d3.select(".outer").append("svg")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.right + ")")
    .call(zoom);

var rect = svg.append("rect")
    .attr("width", width)
    .attr("height", height)
    .style("fill", "none")
    .style("pointer-events", "all");

var container = svg.append("g");

d3.json("./objects.json", function(error, graph) {
  var nodes = graph.nodes.slice(),
      links = [],
      bilinks = [];

  graph.links.forEach(function(link) {
    var s = nodes[link.source],
        t = nodes[link.target],
        i = {}; // intermediate node
    nodes.push(i);
    links.push({source: s, target: i}, {source: i, target: t});
    bilinks.push([s, i, t]);
  });

  force
      .nodes(nodes)
      .links(links)
      .start();

  var link = container.selectAll(".link")
      .data(bilinks)
    .enter().append("path")
      .attr("class", "link");


 var gnodes = container.selectAll('g.gnode')
     .data(graph.nodes)
     .enter()
     .append('g')
     .classed('gnode', true);

var node = gnodes.append("circle")
      .attr("class", "node")
      .attr("r", 2)
      .style("fill", function(d) { return color(d.group); });

  var labels = gnodes.append("text")
  .attr('class', 'text')
      .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("d", function(d) {
      return "M" + d[0].x + "," + d[0].y
          + "S" + d[1].x + "," + d[1].y
          + " " + d[2].x + "," + d[2].y;
    });
    gnodes.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  });
});
