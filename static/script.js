$('#submit').click(function() {

    const column = $('#column').val();
    const regex = $('#regex').val();
    const size = $('#size').val();
    const position = $('#position').val();
    const data = {
        column: column,
        regex: regex,
        size: size,
        position: position
    };

    $('#submit_group').empty()
    .append('<button type="button" class="btn btn-primary" id="next">Next</button>')
    .append('<button type="button" class="btn btn-primary" id="previous">Previous</button>');

    $.ajax({
        type: 'GET',
        url: 'pandas/?fields=' + data.fields.join(',') + '&filter_methods=' + data.filter_methods.join(',') + '&values=' + data.values.join(',') + '&position=' + data.position,
        contentType: 'application/json',
        success: function(data) {
            console.log(data);
            let csvData = jsonToCsv(data["data"]);
            let blob = new Blob([csvData], { type: 'text/csv' });
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.href = url;
            a.download = 'data.csv';
            document.body.appendChild(a);
            a.click();
            window.location.href = url;
        },
        error: function(error) {
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