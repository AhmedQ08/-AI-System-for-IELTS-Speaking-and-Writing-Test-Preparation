document.addEventListener("DOMContentLoaded", function() {
    var score = parseInt(document.getElementById('response-score').textContent);
    
    var width = 250,
        height = 250;

    var outerRadius = width / 2;
    var innerRadius = 80;

    var data = [score];
    var pie = d3.layout.pie().value(function(d) {
        return d;
    });

    var endAng = function(d) {
        return (d / 10) * Math.PI * 2;
    };

    var bgArc = d3.svg
        .arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius)
        .startAngle(0)
        .endAngle(Math.PI * 2);

    var dataArc = d3.svg
        .arc()
        .innerRadius(innerRadius)
        .outerRadius(outerRadius)
        .cornerRadius(15)
        .startAngle(0);

    var svg = d3
        .select('.chart-area')
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var path = svg
        .selectAll("g")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    path
        .append("path")
        .attr("d", bgArc)
        .style("stroke-width", 5)
        .attr("fill", "rgba(0,0,0,0.2)");

    path
        .append("path")
        .attr("fill", "url(#linear-gradient)") // Using linear gradient for radiant color
        .transition()
        .ease("ease-in-out")
        .duration(750)
        .attrTween("d", arcTween);

    path
        .append("text")
        .attr("fill", "#fff")
        .attr("font-size","1em")
        .attr("text-anchor", "middle")
        .attr("x", 0)
        .attr("y", 8)
        .transition()
        .ease("ease-in-out")
        .duration(750)
        .attr("fill", "#000")
        .text(function(d) { return  d.data+ "\nBand " ; }); 

    // Define the linear gradient
    var defs = svg.append("defs");
    var gradient = defs.append("linearGradient")
        .attr("id", "linear-gradient")
        .attr("x1", "0%")   // start x
        .attr("y1", "0%")   // start y
        .attr("x2", "100%") // end x
        .attr("y2", "100%") // end y
        .selectAll("stop")
        .data([
            {offset: "0%", color: "#FFA500"},  // start color
            {offset: "100%", color: "#FFFF00"} // end color
        ])
        .enter().append("stop")
        .attr("offset", function(d) { return d.offset; })
        .attr("stop-color", function(d) { return d.color; });

    function arcTween(d) {
        var interpolate = d3.interpolate(d.startAngle, endAng(d.data));
        return function(t) {
            d.endAngle = interpolate(t);
            return dataArc(d);
        };
    }
});
