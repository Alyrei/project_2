// Plot the default route once the page loads
var defaultURL = "/measles_cases";
d3.json(defaultURL).then(function(data) {
  var data = [data];
  var layout = { margin: { t: 30, b: 100 } };

  var layout = {
    margin: { t: 30, b: 100 },
    title: {
      //text:'USA',
      // text:'Brazil',
      // text:'Austria',
      text:'China',
      // text:'India',
      font: {
        family: 'Courier New, monospace',
        size: 24
      },
      xref: 'paper',
      x: 0.05,
    },
    xaxis: {
      title: {
        text: 'Year',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      },
    },
    yaxis: {
      title: {
        text: 'Total Polio Cases',
        font: {
          family: 'Courier New, monospace',
          size: 18,
          color: '#7f7f7f'
        }
      }
    }
  }




  Plotly.plot("plot_graph", data, layout);
});

// Update the plot with new data
function updatePlotly(newdata) {
  Plotly.restyle("plot_graph", "x", [newdata.x]);
  Plotly.restyle("plot_graph", "y", [newdata.y]);
}

// Get new data whenever the dropdown selection changes
function getData(route) {
  console.log(route);
  d3.json(`/${route}`).then(function(data) {
    console.log("newdata", data);
    updatePlotly(data);
  });
}

