let next_url = undefined;

$('#submit').click(function() {

    $('#submit').text("loading...");

    const column = $('#column').val();
    const regex = $('#regex').val();
    const size = $('#size').val();
    const data = {
        column: column,
        regex: regex,
        size: size,
        position: "1"
    };

    $.ajax({
        type: 'GET',
        url: 'pandas/?column=' + data.column + '&regex=' + data.regex + '&size=' + data.size + '&position=' + data.position,
        contentType: 'application/json',
        success: function(data) {
            $('#submit').text("Submit");

            let csvData = jsonToCsv(data["data"]);
            let blob = new Blob([csvData], { type: 'text/csv' });
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'data.csv';
            document.body.appendChild(a);
            a.click();
            window.location.href = url;

            next_url = data["next_data_link"];

            $('#submit').text("Submit");

        },
        error: function(error) {
            $('#submit').text("Submit");

            console.log(error);
        }
    });

});



$('#next-btn').click(function() {


    if(next_url==undefined) {
        alert("no next url found");
        return;
    }

    $('#next-btn').text("loading...");


    $.ajax({
        type: 'GET',
        url: next_url,
        contentType: 'application/json',
        success: function(data) {
            $('#next-btn').text("Next");

            let csvData = jsonToCsv(data["data"]);
            let blob = new Blob([csvData], { type: 'text/csv' });
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'data.csv';
            document.body.appendChild(a);
            a.click();
            window.location.href = url;

            next_url = data["next_data_link"];


        },
        error: function(error) {
            $('#next-btn').text("Next");

            console.log(error);
        }
    });

});




function jsonToCsv(jsonData) {
    let csv = '';
    // Get the headers
    let headers = Object.keys(jsonData[0]);
    csv += headers.join(',') + '\n';
    // Add the data
    jsonData.forEach(function (row) {
        let data = headers.map(header => JSON.stringify(row[header])).join(','); // Add JSON.stringify statement
        csv += data + '\n';
    });
    return csv;
}

