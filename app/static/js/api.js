// This file handles all the requests to the api
// Author Cory Sabol
// No need to really get fancy in here with all that oop stuff

var xhr = new XMLHttpRequest();
var url = "/apiv1/plot";

// Define our own functionality to the submit button
var sub_data = function () {
    // Get the data from the form
    var xdata = document.getElementById("data_x").value;
    var ydata = document.getElementById("data_y").value;
    var postdata = {};
    var plottype = document.getElementsByName("plotselect")[0].value;

    xhr.open("PUT", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Make sure this is correct or the rest of the code won't work.
    xhr.responseType = "text";

    // We need to prepare the right type of data
    if (["multi_line", "patch"].indexOf(plottype) >= 0) {
        postdata = {data : {x : [xdata], y : [ydata]}, type : plottype};
    } else {
        postdata = {data : {x : xdata, y : ydata}, type : plottype};
    }
    console.log(postdata);
    xhr.send(JSON.stringify(postdata));

    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if(xhr.status == 200) {
                // Get the returned html
                console.log("Got response");
                console.log(xhr);
                console.log(xhr.response);
                console.log(xhr.responseText);
                document.getElementById("plot-container").innerHTML = xhr.responseText;
                var node = document.getElementById("plotscript");
                // This is evil, but necessary for now...
                eval(node.innerHTML);
            }
        }
    };
};

// validate the data input form
var validate_form = function() {
    var form = document.getElementById("data_form");
    var plottype = document.getElementsByName("plotselect").value;
};
