// This file handles all the requests to the api
// Author Cory Sabol
// No need to really get fancy in here with all that oop stuff

var xhr = new XMLHttpRequest();
var url = "/apiv1/plot";
// Get the plot div
var plot_div = document.getElementById("plot-container");

// Define our own functionality to the submit button
var sub_data = function () {
    // Get the data from the form
    var params = document.getElementById("data_input").value;
    console.log(params);
    console.log(JSON.stringify(params));

    xhr.open("PUT", url);
    xhr.setRequestHeader("ContentType", "application/json;charset=UTF-8");
    xhr.responseType = "document";
    xhr.send(JSON.stringify({data : params}));

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.statusCode == 200) {
            // Do a thing
            console.log("it's kind of working");
        }
    };
};
