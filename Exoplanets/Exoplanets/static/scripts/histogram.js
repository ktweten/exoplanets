
(function () {
    'use strict';

    function add_histograms() {
        var histogram_data = [{ 'type': 'radius', 'unit': 'Earth Radii' },
                     { 'type': 'mass', 'unit': 'Earth Masses' },
                     { 'type': 'distance', 'unit': 'Parsecs' }];
        histogram_data.forEach(function (data) {
            d3.json("/" + data.type + "_data", data_callback(data));
        });
    }

    function data_callback(input) {
        var data = input;
        return function (error, response) {
            // Parse the JSON array
            var parsed = JSON.parse(response.data);

            // Extract only the values
            var values = parsed.map(function (entry) { return entry[data.type]; });

            // Define the bounds for the graph svg
            var bounds = { top: 250, right: 450, bottom: 50, left: 50 };

            // Calculate the number of bins for the histogram from the extent of the input
            var maxvalue = Math.ceil(Math.max.apply(null, values));
            var num_bins = Math.min(maxvalue, 100);
            var graph;

            // Each histogram will be appended to the histograms div
            d3.select("#histograms").append("div")
                .attr("class", "details-head row depth-2")
                .append("h2")
                .text(data.type.charAt(0).toUpperCase() + data.type.slice(1));

            // Create the svg for drawing the histogram
            graph = d3.select("#histograms").append("div")
               .attr("class", "details row depth-1")
               .append("svg")
               .attr("class", "histogram depth-2")
               .attr("viewBox", "0, 0, 500, 300");

            // Add the units to the x axis
            graph.append("text")
                .attr("transform", "translate(250, 290)")
                .style("text-anchor", "middle")
                .text(data.unit);

             make_histogram(values, bounds, graph, num_bins);
        }
    }

    function make_histogram(values, bounds, graph, num_bins) {
        // Calculate the width of each bar from the size of the svg and number of bins
        var width = (bounds.right - bounds.left) / num_bins;

        // Set the domain and range of x values
        var x = d3.scale.linear()
            .domain(d3.extent(values))
            .range([bounds.left, bounds.right]);

        // Split the data values into the calculated bins
        var scale = d3.scale.linear().domain([0, num_bins]).range(d3.extent(values));
        var ticks = d3.range(num_bins + 1).map(scale);
        var binned = d3.layout.histogram().bins(ticks)(values);

        // Set the domain and range for the y values from the size of the largest bin
        var maxbin = d3.max(binned, function (entry) { return entry.length; });
        var y = d3.scale.linear()
            .domain([0, maxbin])
            .range([bounds.top, bounds.bottom]);

        // Align the x and y axis
        var yAxis = d3.svg.axis().scale(y).orient("left");
        var xAxis = d3.svg.axis().scale(x).orient("bottom");

        graph.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .attr("transform", "translate(" + bounds.left + ", 0)");

        graph.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + bounds.top + ")")
            .call(xAxis);

        // Add each bar to the histogram
        graph.selectAll(".bar")
            .data(binned)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function (entry) { return x(entry.x); })
            .attr("width", width)
            .attr("y", function (entry) { return y(entry.y); })
            .attr("fill", "gray")
            .attr("height", function (entry) { return bounds.top - y(entry.y); });
    }

    function error() {
        console.log("Error");
    }

    add_histograms();
})();
