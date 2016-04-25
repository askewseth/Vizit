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
    console.log(xdata + " " + ydata);
    console.log(JSON.stringify({data : {x : xdata, y : ydata}}));

    xhr.open("PUT", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    // Make sure this is correct or the rest of the code won't work.
    xhr.responseType = "text";
    xhr.send(JSON.stringify({data : {x : xdata, y : ydata}}));

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
