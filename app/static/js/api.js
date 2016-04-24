// This file handles all the requests to the api
// Author Cory Sabol
// No need to really get fancy in here with all that oop stuff

var xhr = new XMLHttpRequest();
var url = "/apiv1/plot";

// Define our own functionality to the submit button
var sub_data = function () {
    // Get the data from the form
    var params = document.getElementById("data_input").value;
    console.log(params);
    console.log(JSON.stringify({data : params}));

    xhr.open("PUT", url, true);
    xhr.setRequestHeader("ContentType", "application/json;charset=UTF-8");
    // Make sure this is correct or the rest of the code won't work.
    xhr.responseType = "text";
    xhr.send(JSON.stringify({data : params}));

    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if(xhr.status == 200) {
                // Get the returned html
                console.log("Got response");
                console.log(xhr);
                console.log(xhr.response);
                console.log(xhr.responseText);
                document.getElementById("plot-container").innerHTML = xhr.responseText;
            }
        }
    };
};
