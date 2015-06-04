(function () {
    'use strict';

    if (radius) {
        var base = { radius: 1.0, offset: 0, colour: colour },
            other = { radius: radius, offset: 120, colour: "white" },
            dataset = [base, other],
            padding = 15;

        var svg = d3.select(tag);
        var bodies = svg.selectAll("circle")
            .data(dataset)
            .enter()
            .append("circle");

        if (base.radius < other.radius) {
            base.radius = 50 / other.radius;
            other.radius = 50;
        } else {
            other.radius = 50 * other.radius;
            base.radius = 50;
        }

        bodies.attr("cx", function (d) {
                return padding + d.offset + d.radius;
            })
            .attr("cy", 125)
            .attr("r", function (d) {
                return d.radius;
            })
            .attr("stroke", "black")
            .attr("stroke-width", "1")
            .attr("fill", function (d) { return d.colour; });
    }
})();